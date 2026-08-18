"""
Mapbox Vector Tile (MVT) API Endpoints.

Provides high-performance vector tile endpoints for the interactive map.
Optimized for Vercel serverless architecture with Edge Caching and Redis caching.

Endpoints:
- /api/tiles/<z>/<x>/<y>.pbf - Single layer tile endpoint
- /api/tiles/combined/<z>/<x>/<y>.pbf - Multi-layer combined tile endpoint
- /api/tiles/layers - List available tile layers

Architecture:
- Generates tiles on-demand using PostGIS ST_AsMVT
- Caches tiles in Redis (Upstash) for fast repeat access
- Sets Vercel Edge Cache headers for CDN distribution
- Response time: < 50ms for cached tiles, < 200ms for uncached
"""

from flask import Blueprint, jsonify, request, make_response, current_app
from flask_login import login_required, current_user
from extensions import limiter
import logging
from datetime import datetime, timedelta
from typing import Optional
import hashlib

logger = logging.getLogger(__name__)

# Create blueprint
map_bp = Blueprint("map_tiles", __name__, url_prefix="/api/tiles")

# Import tile generator
from utils.tile_generator import (
    generate_mvt_tile,
    generate_multi_layer_mvt,
    LAYER_CONFIG,
    get_tile_cache_key,
)

def get_redis_client():
    """Returns the global Redis client from the current application context."""
    return getattr(current_app, 'redis_client', None)


def get_tile_from_cache(cache_key: str) -> Optional[bytes]:
    """Retrieve tile from Redis cache."""
    redis_client = get_redis_client()
    if not redis_client:
        return None

    try:
        cached = redis_client.get(cache_key)
        if cached:
            logger.debug(f"Cache hit for {cache_key}")
            return cached
        logger.debug(f"Cache miss for {cache_key}")
        return None
    except Exception as e:
        logger.error(f"Redis cache get error: {e}")
        return None


def set_tile_in_cache(cache_key: str, tile_data: bytes, ttl: int = 3600) -> None:
    """Store tile in Redis cache with TTL."""
    redis_client = get_redis_client()
    if not redis_client:
        return

    try:
        redis_client.setex(cache_key, ttl, tile_data)
        logger.debug(f"Cached tile {cache_key} for {ttl}s")
    except Exception as e:
        logger.error(f"Redis cache set error: {e}")


@map_bp.route("/<int:z>/<int:x>/<int:y>.pbf", methods=["GET"])
@limiter.limit("2000 per minute")
def get_tile(z: int, x: int, y: int):
    """
    Get a Mapbox Vector Tile for the specified coordinates.

    URL Parameters:
        z: Zoom level (0-20)
        x: Tile X coordinate
        y: Tile Y coordinate

    Query Parameters:
        layer: Layer name (default: 'attractions')
               Options: attractions, natural_heritage, built_heritage, events

    Returns:
        Binary MVT tile (application/x-protobuf)

    Response Headers:
        Cache-Control: public, s-maxage=3600, stale-while-revalidate=86400
        Content-Type: application/x-protobuf
        ETag: Hash of tile content for conditional requests
    """
    # Validate zoom level
    if z < 0 or z > 20:
        return jsonify({"error": "Zoom level must be between 0 and 20"}), 400

    # Get layer from query parameter
    layer_name = request.args.get("layer", "attractions")

    if layer_name not in LAYER_CONFIG:
        return jsonify({
            "error": f"Unknown layer: {layer_name}",
            "available_layers": list(LAYER_CONFIG.keys())
        }), 400

    # Generate cache key
    cache_key = get_tile_cache_key(z, x, y, layer_name)

    # Try to get from cache first
    cached_tile = get_tile_from_cache(cache_key)
    if cached_tile is not None:
        response = make_response(cached_tile)
        response.headers["Content-Type"] = "application/x-protobuf"
        response.headers["X-Cache"] = "HIT"
        _add_cache_headers(response, is_cached=True)
        return response

    # Generate tile
    tile_data = generate_mvt_tile(z, x, y, layer_name)

    if tile_data is None:
        return jsonify({"error": "Failed to generate tile"}), 500

    # Cache the tile
    if tile_data:  # Only cache non-empty tiles
        set_tile_in_cache(cache_key, tile_data)

    # Create response
    response = make_response(tile_data)
    response.headers["Content-Type"] = "application/x-protobuf"
    response.headers["X-Cache"] = "MISS"
    response.headers["ETag"] = f'"{hashlib.md5(tile_data).hexdigest()}"'
    _add_cache_headers(response, is_cached=False)

    logger.info(
        f"Served MVT tile: {layer_name}/{z}/{x}/{y} "
        f"({len(tile_data)} bytes, cache={response.headers['X-Cache']})"
    )

    return response


@map_bp.route("/combined/<int:z>/<int:x>/<int:y>.pbf", methods=["GET"])
@limiter.limit("2000 per minute")
def get_combined_tile(z: int, x: int, y: int):
    """
    Get a combined Mapbox Vector Tile with multiple layers.

    URL Parameters:
        z: Zoom level (0-20)
        x: Tile X coordinate
        y: Tile Y coordinate

    Query Parameters:
        layers: Comma-separated list of layer names
                (default: all available layers)

    Returns:
        Binary MVT tile with multiple named layers

    Example:
        GET /api/tiles/combined/12/500/500.pbf?layers=attractions,natural_heritage
    """
    # Validate zoom level
    if z < 0 or z > 20:
        return jsonify({"error": "Zoom level must be between 0 and 20"}), 400

    # Get requested layers
    layers_param = request.args.get("layers", "")
    if layers_param:
        layer_names = [l.strip() for l in layers_param.split(",")]
        # Validate layer names
        invalid_layers = [l for l in layer_names if l not in LAYER_CONFIG]
        if invalid_layers:
            return jsonify({
                "error": f"Unknown layers: {invalid_layers}",
                "available_layers": list(LAYER_CONFIG.keys())
            }), 400
    else:
        layer_names = list(LAYER_CONFIG.keys())

    # Generate cache key
    layers_str = ",".join(sorted(layer_names))
    cache_key = f"mvt:combined:{layers_str}:{z}:{x}:{y}"

    # Try cache first
    cached_tile = get_tile_from_cache(cache_key)
    if cached_tile is not None:
        response = make_response(cached_tile)
        response.headers["Content-Type"] = "application/x-protobuf"
        response.headers["X-Cache"] = "HIT"
        _add_cache_headers(response, is_cached=True)
        return response

    # Generate combined tile
    tile_data = generate_multi_layer_mvt(z, x, y, layer_names)

    if tile_data is None:
        return jsonify({"error": "Failed to generate combined tile"}), 500

    # Cache the tile
    if tile_data:
        set_tile_in_cache(cache_key, tile_data, ttl=3600)

    # Create response
    response = make_response(tile_data)
    response.headers["Content-Type"] = "application/x-protobuf"
    response.headers["X-Cache"] = "MISS"
    response.headers["ETag"] = f'"{hashlib.md5(tile_data).hexdigest()}"'
    _add_cache_headers(response, is_cached=False)

    logger.info(
        f"Served combined MVT tile: {layers_str}/{z}/{x}/{y} "
        f"({len(tile_data)} bytes, cache={response.headers['X-Cache']})"
    )

    return response


@map_bp.route("/layers", methods=["GET"])
@limiter.limit("30 per minute")
def get_available_layers():
    """
    Get information about available tile layers.

    Returns:
        JSON object with layer metadata
    """
    layers = []
    for name, config in LAYER_CONFIG.items():
        layers.append({
            "name": name,
            "table": config["table"],
            "id_column": config["id_column"],
            "name_column": config["name_column"],
            "category_column": config["category_column"],
        })

    response = jsonify({"layers": layers})
    response.headers["Cache-Control"] = "public, max-age=300"
    return response


@map_bp.route("/cache/invalidate", methods=["POST"])
@limiter.limit("10 per hour")
@login_required
def invalidate_cache():
    """
    Invalidate cached tiles for a specific layer.

    This endpoint should be called when heritage/attraction data is updated
    to ensure fresh tiles are generated.

    Request Body (JSON):
        layer: Layer name to invalidate (required)
        z: Optional zoom level to invalidate (default: all)
        x, y: Optional specific tile coordinates

    Returns:
        JSON status object
    """
    # Only admins may invalidate the tile cache.
    if current_user.role != "admin":
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    layer_name = data.get("layer")
    if not layer_name:
        return jsonify({"error": "Layer name required"}), 400

    if layer_name not in LAYER_CONFIG:
        return jsonify({
            "error": f"Unknown layer: {layer_name}",
            "available_layers": list(LAYER_CONFIG.keys())
        }), 400

    redis_client = get_redis_client()
    if not redis_client:
        return jsonify({
            "status": "warning",
            "message": "Redis caching not enabled, no cache to invalidate"
        }), 200

    try:
        # Build pattern for cache key — validate z/x/y are integers or "*".
        def _validate_coord(val, name):
            if val is None or val == "*":
                return "*"
            try:
                return str(int(val))
            except (ValueError, TypeError):
                raise ValueError(f"Invalid {name} value: must be an integer or '*'")

        try:
            z = _validate_coord(data.get("z"), "z")
            x = _validate_coord(data.get("x"), "x")
            y = _validate_coord(data.get("y"), "y")
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400

        pattern = f"mvt:{layer_name}:{z}:{x}:{y}"

        # Use SCAN instead of KEYS to avoid blocking the Redis server.
        keys = []
        cursor = 0
        while True:
            cursor, batch = redis_client.scan(cursor=cursor, match=pattern, count=100)
            keys.extend(batch)
            if cursor == 0:
                break

        if keys:
            redis_client.delete(*keys)
            logger.info(f"Invalidated {len(keys)} cache keys for layer {layer_name}")
            return jsonify({
                "status": "success",
                "message": f"Invalidated {len(keys)} cached tiles",
                "layer": layer_name
            })
        else:
            return jsonify({
                "status": "success",
                "message": "No cached tiles found for this layer",
                "layer": layer_name
            })

    except Exception as e:
        logger.error(f"Cache invalidation error: {e}")
        return jsonify({"error": str(e)}), 500


def _add_cache_headers(response, is_cached: bool = False) -> None:
    """
    Add Vercel Edge Cache headers to response.

    Args:
        response: Flask response object
        is_cached: Whether the tile was served from Redis cache
    """
    if is_cached:
        # Already cached in Redis, shorter Edge Cache TTL
        response.headers["Cache-Control"] = (
            "public, s-maxage=600, stale-while-revalidate=3600"
        )
    else:
        # Fresh from database, longer Edge Cache TTL
        response.headers["Cache-Control"] = (
            "public, s-maxage=3600, stale-while-revalidate=86400"
        )

    # Additional headers for CDN optimization
    response.headers["Vary"] = "Accept-Encoding"
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Set expiry header
    expires = datetime.utcnow() + timedelta(hours=1)
    response.headers["Expires"] = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")


# Register cache invalidation hook when attractions/heritage are updated
def register_cache_invalidation_hooks(app):
    """
    Register hooks to invalidate map tile cache when data changes.

    This should be called in app.py to automatically invalidate
    cached tiles when attractions or heritage items are updated.
    """
    from flask import g

    @app.teardown_appcontext
    def invalidate_on_data_change(exception=None):
        """Invalidate cache if data was modified during request."""
        if not hasattr(g, "data_modified"):
            return

        if exception:
            return

        # Invalidate all map tile layers
        redis_client = get_redis_client()
        if redis_client:
            try:
                # Pattern to match all MVT cache keys — use SCAN to avoid blocking.
                pattern = "mvt:*"
                keys = []
                cursor = 0
                while True:
                    cursor, batch = redis_client.scan(cursor=cursor, match=pattern, count=100)
                    keys.extend(batch)
                    if cursor == 0:
                        break
                if keys:
                    redis_client.delete(*keys)
                    logger.info(f"Invalidated {len(keys)} map tile cache entries")
            except Exception as e:
                logger.error(f"Cache invalidation on teardown: {e}")
