"""
Route Optimization API Endpoints (OSRM).

Provides REST API for multi-stop route optimization using public OSRM.
Proxies requests through Flask.

Endpoints:
- POST /api/v1/routing/optimize — Optimize multi-stop route
- POST /api/v1/routing/directions — Get directions between waypoints
- GET  /api/v1/routing/suggested — Get pre-defined suggested routes
"""

import json
import logging

import requests
from flask import Blueprint, current_app, jsonify, request

from extensions import limiter

from .routing import (
    OSRM_BASE_URL,
    build_cache_key,
    get_suggested_routes,
    parse_optimization_response,
)

logger = logging.getLogger(__name__)

routing_bp = Blueprint("routing", __name__, url_prefix="/api/v1/routing")


def _get_redis_client():
    return getattr(current_app, "redis_client", None)


def _get_cached_route(cache_key: str):
    redis_client = _get_redis_client()
    if not redis_client:
        return None
    try:
        cached = redis_client.get(cache_key)
        if cached:
            logger.debug(f"Route cache hit: {cache_key}")
            if isinstance(cached, bytes):
                cached = cached.decode("utf-8")
            return json.loads(cached)
        return None
    except Exception as e:
        logger.error(f"Redis route cache get error: {e}")
        return None


def _set_cached_route(cache_key: str, data: dict, ttl: int = 3600):
    redis_client = _get_redis_client()
    if not redis_client:
        return
    try:
        redis_client.setex(cache_key, ttl, json.dumps(data))
    except Exception as e:
        logger.error(f"Redis route cache set error: {e}")


@routing_bp.route("/optimize", methods=["POST"])
@limiter.limit("5 per minute")  # Strict rate limit for public OSRM
def optimize_route():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Request body required"}), 400

    attraction_ids = data.get("attraction_ids", [])
    start_coords = data.get("start")
    profile = "driving" # OSRM public trip endpoint defaults to driving
    round_trip = data.get("round_trip", True)

    if not attraction_ids or len(attraction_ids) < 2:
        return jsonify({"success": False, "error": "At least 2 attraction IDs required"}), 400
    if len(attraction_ids) > 20: # Keep it low for OSRM public
        return jsonify({"success": False, "error": "Maximum 20 stops supported"}), 400
    if not start_coords or "lng" not in start_coords or "lat" not in start_coords:
        return jsonify({"success": False, "error": "Start coordinates required"}), 400

    cache_key = build_cache_key(attraction_ids, start_coords, profile, round_trip)
    cached_result = _get_cached_route(cache_key)
    if cached_result:
        cached_result["cached"] = True
        return jsonify(cached_result)

    try:
        from modules.attractions.models import Attraction
        attractions = (
            Attraction.query.filter(
                Attraction.id.in_(attraction_ids), Attraction.status == "approved"
            ).all()
        )
        if len(attractions) < 2:
            return jsonify({"success": False, "error": "Not enough valid attractions found"}), 400

        attraction_dicts = []
        # Sort to match IDs order if possible, or just build the list
        for attr in attractions:
            attraction_dicts.append({
                "id": attr.id,
                "name": attr.name,
                "latitude": attr.latitude,
                "longitude": attr.longitude,
                "category": attr.category,
            })
    except Exception as e:
        logger.error(f"Database error: {e}")
        return jsonify({"success": False, "error": "Failed to fetch data"}), 500

    # Build OSRM coordinate string: "lng,lat;lng,lat"
    coords = [f"{start_coords['lng']},{start_coords['lat']}"]
    for attr in attraction_dicts:
        coords.append(f"{attr['longitude']},{attr['latitude']}")
    
    coords_str = ";".join(coords)
    
    # OSRM trip API endpoint
    # source=first ensures the start_coords is always the start of the trip
    # roundtrip=true returns to start
    url = f"{OSRM_BASE_URL}/trip/v1/driving/{coords_str}?source=first&roundtrip={str(round_trip).lower()}&geometries=geojson&overview=full"

    try:
        osrm_response = requests.get(url, timeout=15)
        
        if osrm_response.status_code == 429:
            return jsonify({"success": False, "error": "OSRM server busy. Try later."}), 429
            
        if osrm_response.status_code != 200:
            return jsonify({"success": False, "error": "OSRM service error"}), 502

        osrm_data = osrm_response.json()

    except requests.exceptions.RequestException as e:
        logger.error(f"OSRM request failed: {e}")
        return jsonify({"success": False, "error": "Optimization service unavailable"}), 502

    result = parse_optimization_response(osrm_data, attraction_dicts, start_coords, round_trip)
    if not result:
        return jsonify({"success": False, "error": "Failed to parse result"}), 500

    _set_cached_route(cache_key, result, ttl=3600)
    result["cached"] = False
    return jsonify(result)


@routing_bp.route("/directions", methods=["POST"])
@limiter.limit("10 per minute")
def get_directions():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Request body required"}), 400

    coordinates = data.get("coordinates", [])
    if len(coordinates) < 2:
        return jsonify({"success": False, "error": "At least 2 coordinate pairs required"}), 400

    coords_str = ";".join([f"{c[0]},{c[1]}" for c in coordinates])
    url = f"{OSRM_BASE_URL}/route/v1/driving/{coords_str}?geometries=geojson&overview=full"

    try:
        osrm_response = requests.get(url, timeout=10)
        if osrm_response.status_code != 200:
            return jsonify({"success": False, "error": "Directions service unavailable"}), 502

        geojson_data = osrm_response.json()
        routes = geojson_data.get("routes", [])
        if not routes:
            return jsonify({"success": False, "error": "No route found"}), 404

        route = routes[0]
        return jsonify({
            "success": True,
            "geometry": route.get("geometry", {}),
            "summary": {
                "distance_km": round(route.get("distance", 0) / 1000, 1),
                "duration_minutes": round(route.get("duration", 0) / 60),
            },
        })

    except requests.exceptions.RequestException as e:
        logger.error(f"OSRM Directions request failed: {e}")
        return jsonify({"success": False, "error": "Directions service unavailable"}), 502


@routing_bp.route("/suggested", methods=["GET"])
@limiter.limit("30 per minute")
def get_suggested():
    routes = get_suggested_routes()
    enriched_routes = []
    
    for route in routes:
        enriched = dict(route)
        try:
            from modules.attractions.models import Attraction
            if route.get("attraction_names"):
                attractions = []
                for name in route["attraction_names"]:
                    attr = Attraction.query.filter(
                        Attraction.name.ilike(f"%{name}%"),
                        Attraction.status == "approved"
                    ).first()
                    if attr:
                        attractions.append({
                            "id": attr.id,
                            "name": attr.name,
                            "latitude": attr.latitude,
                            "longitude": attr.longitude,
                            "category": attr.category,
                        })
                enriched["attractions"] = attractions
        except Exception:
            enriched["attractions"] = []
        enriched_routes.append(enriched)

    return jsonify({"success": True, "routes": enriched_routes})
