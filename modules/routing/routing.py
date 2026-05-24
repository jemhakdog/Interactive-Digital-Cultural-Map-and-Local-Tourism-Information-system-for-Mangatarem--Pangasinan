"""
Route Optimization Service using OSRM Public API.

This module uses the Open Source Routing Machine (OSRM) public demo server
to solve the Traveling Salesman Problem (TSP) for tourist itineraries.
- No API key is required.
- Results are cached in Upstash Redis to conserve the strict 1 req/s rate limit.
"""

import os
import json
import hashlib
import logging
from typing import Optional
import polyline

logger = logging.getLogger(__name__)

# OSRM Public API base URL
OSRM_BASE_URL = "http://router.project-osrm.org"

# Suggested tourist routes for Mangatarem
SUGGESTED_ROUTES = [
    {
        "id": "nature-trail",
        "name": "The Nature Lover's Trail",
        "description": "Discover Mangatarem's natural wonders — springs, falls, and forest trails.",
        "color": "#10b981",
        "icon": "🌿",
        "profile": "driving-car",
        "attraction_names": [
            "Manleluag Spring National Park",
            "Timmanguyob Falls",
            "Daang Kalikasan Trail",
        ],
        "estimated_duration_min": 120,
        "estimated_distance_km": 25,
    },
    {
        "id": "heritage-walk",
        "name": "Historical Heritage Walk",
        "description": "Walk through centuries of history — churches, plazas, and colonial architecture.",
        "color": "#f59e0b",
        "icon": "🏛️",
        "profile": "foot-walking",
        "attraction_names": [
            "St. Raymund de Peñafort Church",
            "Municipal Town Plaza",
            "Old Municipal Hall",
        ],
        "estimated_duration_min": 60,
        "estimated_distance_km": 2,
    },
]


def build_cache_key(
    attraction_ids: list,
    start_coords: dict,
    profile: str,
    round_trip: bool,
) -> str:
    """Build a deterministic cache key for an optimization request."""
    key_data = {
        "ids": sorted(attraction_ids),
        "start": [round(start_coords["lng"], 4), round(start_coords["lat"], 4)],
        "profile": profile,
        "round_trip": round_trip,
    }
    key_str = json.dumps(key_data, sort_keys=True)
    key_hash = hashlib.md5(key_str.encode()).hexdigest()
    return f"route_opt_osrm:{key_hash}"


def parse_optimization_response(
    osrm_response: dict, attractions: list, start_coords: dict, round_trip: bool
) -> Optional[dict]:
    """
    Parse the OSRM trip response into a frontend-friendly format.
    """
    if not osrm_response or osrm_response.get("code") != "Ok":
        logger.error(f"OSRM optimization failed: {osrm_response.get('message', 'Unknown')}")
        return None

    trips = osrm_response.get("trips", [])
    if not trips:
        logger.warning("OSRM returned no trips")
        return None

    trip = trips[0]
    waypoints = osrm_response.get("waypoints", [])
    
    # Sort waypoints by their optimized order (waypoint_index)
    sorted_waypoints = sorted(waypoints, key=lambda w: w.get("waypoint_index", 0))

    optimized_order = []
    # OSRM includes the start coordinate as a waypoint. We need to match the others to attractions.
    # The first coordinate was the start point.
    
    current_time_s = 0
    # Create a mapping of original index to attraction
    # Original list passed to OSRM: [start] + attractions
    for wp in sorted_waypoints:
        orig_index = wp.get("trips_index", 0)
        # Skip the start coordinate from the final stop list unless it's the end of a round trip?
        # Let's just map original index > 0 to the attractions array (0 is the start point).
        if orig_index > 0 and orig_index - 1 < len(attractions):
            attr = attractions[orig_index - 1]
            # Estimate arrival time based on leg durations
            
            optimized_order.append(
                {
                    "id": attr.get("id"),
                    "name": attr.get("name", "Unknown"),
                    "latitude": attr.get("latitude"),
                    "longitude": attr.get("longitude"),
                    "image": attr.get("image", ""),
                    "category": attr.get("category", ""),
                    "arrival_seconds": current_time_s,
                    "arrival_minutes": round(current_time_s / 60),
                }
            )
            current_time_s += 600  # Estimate 10 mins service time

    # Extract geometry
    geometry = trip.get("geometry")

    total_distance_m = trip.get("distance", 0)
    total_duration_s = trip.get("duration", 0)

    return {
        "success": True,
        "summary": {
            "duration_minutes": round(total_duration_s / 60),
            "duration_seconds": total_duration_s,
            "distance_km": round(total_distance_m / 1000, 1),
            "distance_meters": total_distance_m,
            "stops": len(optimized_order),
            "unassigned": 0,
        },
        "optimized_order": optimized_order,
        "geometry": geometry,
    }


def get_suggested_routes() -> list:
    """Return pre-defined suggested tourist routes."""
    return SUGGESTED_ROUTES
