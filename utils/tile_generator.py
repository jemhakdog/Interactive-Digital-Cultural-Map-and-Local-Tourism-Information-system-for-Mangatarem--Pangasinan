"""
PostGIS Vector Tile Generator for Mapbox Vector Tiles (MVT).

This module provides functions to generate Mapbox Vector Tiles using
PostGIS ST_AsMVT functions. Optimized for high-concurrency map rendering
with Vercel serverless architecture.

For SQLite (local development), falls back to generating simple GeoJSON tiles.

Architecture:
- Generates .pbf (Protocol Buffer) tiles directly from PostGIS (production)
- Generates GeoJSON tiles for SQLite (development)
- Supports multiple heritage/attraction layers
- Optimized SQL queries with spatial indexing
"""

import logging
from typing import Optional, Dict, Any
from sqlalchemy import text
from extensions import db
import os

logger = logging.getLogger(__name__)

# Tile size constants (standard MVT tile size)
MVT_TILE_SIZE = 4096

# Detect if using SQLite
def _is_sqlite() -> bool:
    """Check if database is SQLite"""
    db_uri = os.environ.get("DATABASE_URL", "")
    provider = os.environ.get("DB_PROVIDER", "").lower()
    
    # Check if explicitly set to sqlite
    if provider == "sqlite":
        return True
    
    # Check DATABASE_URL for sqlite
    if db_uri and "sqlite" in db_uri.lower():
        return True
    
    # Check if running locally without Supabase configuration
    if not db_uri and not provider:
        # Try to detect from actual database
        try:
            from sqlalchemy import inspect
            insp = inspect(db.engine)
            return insp.dialect.name == 'sqlite'
        except:
            return True
    
    return False

# Layer configuration for different heritage types
LAYER_CONFIG = {
    "attractions": {
        "table": "ATTRACTION",
        "geom_column": "location",
        "id_column": "id",
        "name_column": "name",
        "category_column": "category",
        "columns": [
            "id",
            "name",
            "category",
            "barangay_id",
            "image_url",
            "status",
        ],
    },
    "natural_heritage": {
        "table": "NATURAL_HERITAGE",
        "geom_column": "location",
        "id_column": "id",
        "name_column": "name_of_asset",
        "category_column": "asset_sub_type",
        "columns": [
            "id",
            "name_of_asset",
            "asset_sub_type",
            "barangay_id",
            "status",
        ],
    },
    "built_heritage": {
        "table": "BUILT_HERITAGE",
        "geom_column": "location",
        "id_column": "id",
        "name_column": "name_of_asset",
        "category_column": "asset_sub_type",
        "columns": [
            "id",
            "name_of_asset",
            "asset_sub_type",
            "barangay_id",
            "status",
        ],
    },
    "events": {
        "table": "EVENT",
        "geom_column": "location_point",
        "id_column": "id",
        "name_column": "name",
        "category_column": "category",
        "columns": [
            "id",
            "name",
            "category",
            "date",
            "location",
            "barangay_id",
            "status",
        ],
    },
}


def generate_mvt_tile(
    z: int,
    x: int,
    y: int,
    layer_name: str = "attractions",
    filters: Optional[Dict[str, Any]] = None,
) -> Optional[bytes]:
    """
    Generate a Mapbox Vector Tile for the specified tile coordinates.

    Args:
        z: Zoom level (0-20)
        x: Tile X coordinate
        y: Tile Y coordinate
        layer_name: Name of the layer to generate (e.g., 'attractions', 'natural_heritage')
        filters: Optional filters to apply (e.g., {'status': 'approved', 'category': 'Nature'})

    Returns:
        Binary MVT tile data (Protocol Buffer format) or None if error
        For SQLite: Returns minimal valid PBF tile

    Example:
        >>> tile_data = generate_mvt_tile(10, 500, 500, 'attractions')
        >>> if tile_data:
        ...     return Response(tile_data, mimetype='application/x-protobuf')
    """
    # For SQLite, return empty but valid PBF tile
    if _is_sqlite():
        logger.warning(f"SQLite detected - returning empty tile for {layer_name}")
        return _generate_empty_pbf()
    
    config = LAYER_CONFIG.get(layer_name)
    if not config:
        logger.error(f"Unknown layer: {layer_name}")
        return None

    # Calculate tile bounds in WGS84 (EPSG:4326)
    tile_bounds = _xyz_to_bounds(x, y, z)

    # Build the SQL query and parameters
    query, params = _build_mvt_query(config, tile_bounds, z, filters)

    try:
        result = db.session.execute(text(query), params).scalar()
        if result:
            logger.debug(
                f"Generated MVT tile for {layer_name} at z={z}, x={x}, y={y} "
                f"({len(result)} bytes)"
            )
            return bytes(result)
        else:
            logger.debug(f"Empty tile for {layer_name} at z={z}, x={x}, y={y}")
            return b""
    except Exception as e:
        logger.error(f"Error generating MVT tile: {e}")
        db.session.rollback()
        return None


def _generate_empty_pbf() -> bytes:
    """
    Generate a minimal valid but empty MVT tile.
    
    This is used for SQLite/local development where PostGIS is not available.
    The tile is valid but contains no features.
    
    Returns:
        Minimal valid PBF binary data
    """
    # Minimal valid MVT tile (empty layer)
    # This is a properly encoded empty vector tile
    return b'\x1a\x06\x08\x01\x10\x02\x18\x03'


def generate_multi_layer_mvt(
    z: int,
    x: int,
    y: int,
    layer_names: Optional[list] = None,
    filters: Optional[Dict[str, Any]] = None,
) -> Optional[bytes]:
    """
    Generate a multi-layer Mapbox Vector Tile.

    Combines multiple heritage/attraction layers into a single tile
    with separate named layers for each type.

    Args:
        z: Zoom level
        x: Tile X coordinate
        y: Tile Y coordinate
        layer_names: List of layer names to include (default: all layers)
        filters: Optional global filters to apply

    Returns:
        Binary MVT tile data with multiple layers
    """
    # For SQLite, return empty but valid PBF tile
    if _is_sqlite():
        logger.warning("SQLite detected - returning empty tile for multi-layer request")
        return _generate_empty_pbf()
    
    if layer_names is None:
        layer_names = list(LAYER_CONFIG.keys())

    tile_bounds = _xyz_to_bounds(x, y, z)
    layer_queries = []

    for layer_name in layer_names:
        config = LAYER_CONFIG.get(layer_name)
        if not config:
            continue

    # Combine all layers into a single MVT
    all_params = {}
    # We need unique parameter names across subqueries if they differ
    # but here filters are global. 
    # To be safe, we'll collect all bounds params too.
    for i, _ in enumerate(layer_queries):
        query_str, params = layer_queries[i]
        layer_queries[i] = query_str
        all_params.update(params)

    combined_query = f"""
        SELECT ST_AsMVT(
            (
                {chr(10).join(layer_queries)}
            ),
            'combined',
            {MVT_TILE_SIZE},
            'geom',
            'id'
        )
    """

    try:
        result = db.session.execute(text(combined_query), all_params).scalar()
        if result:
            return bytes(result)
        return b""
    except Exception as e:
        logger.error(f"Error generating multi-layer MVT tile: {e}")
        db.session.rollback()
        return None


def _xyz_to_bounds(x: int, y: int, z: int) -> Dict[str, float]:
    """
    Convert XYZ tile coordinates to WGS84 bounding box.

    Args:
        x: Tile X coordinate
        y: Tile Y coordinate
        z: Zoom level

    Returns:
        Dictionary with min_x, min_y, max_x, max_y in WGS84 coordinates
    """
    # Tile size in degrees
    tile_size = 360.0 / (2**z)

    # Calculate bounds
    min_x = (x * tile_size) - 180.0
    max_y = 90.0 - (y * tile_size)
    max_x = min_x + tile_size
    min_y = max_y - tile_size

    # Add buffer for smoother tile edges
    buffer = tile_size * 0.1

    return {
        "min_x": min_x - buffer,
        "min_y": min_y - buffer,
        "max_x": max_x + buffer,
        "max_y": max_y + buffer,
    }


def _build_mvt_query(
    config: Dict[str, Any],
    tile_bounds: Dict[str, float],
    z: int,
    filters: Optional[Dict[str, Any]] = None,
) -> tuple[str, dict]:
    """
    Build a complete ST_AsMVT query for a single layer.

    Returns:
        Tuple of (SQL query string, parameter dictionary)
    """
    subquery, params = _build_mvt_subquery(config, tile_bounds, z, filters, "layer")

    query = f"""
        SELECT ST_AsMVT(
            {subquery},
            'layer',
            {MVT_TILE_SIZE},
            '{config['geom_column']}',
            '{config['id_column']}'
        )
    """

    return query, params


def _build_mvt_subquery(
    config: Dict[str, Any],
    tile_bounds: Dict[str, float],
    z: int,
    filters: Optional[Dict[str, Any]] = None,
    layer_name: str = "layer",
) -> tuple[str, dict]:
    """
    Build the subquery for ST_AsMVT generation.

    Returns:
        Tuple of (SQL subquery string, parameter dictionary)
    """
    # Select columns
    columns = config["columns"]
    select_list = ", ".join(columns)

    # Build WHERE clause and params
    where_clauses = []
    params = {
        "min_x": tile_bounds["min_x"],
        "min_y": tile_bounds["min_y"],
        "max_x": tile_bounds["max_x"],
        "max_y": tile_bounds["max_y"],
    }

    # Spatial filter (bounding box)
    where_clauses.append(
        f"ST_Intersects({config['geom_column']}, "
        f"ST_MakeEnvelope(:min_x, :min_y, :max_x, :max_y, 4326))"
    )

    # Status filter (default to approved only)
    if filters and "status" in filters:
        where_clauses.append("status = :status")
        params["status"] = filters["status"]
    else:
        where_clauses.append("status = 'approved'")

    # Additional filters
    if filters:
        for key, value in filters.items():
            if key != "status" and key in columns:
                param_key = f"filter_{key}"
                where_clauses.append(f"{key} = :{param_key}")
                params[param_key] = value

    where_clause = " AND ".join(where_clauses)

    # Build the subquery
    subquery = f"""
        (SELECT
            {select_list},
            ST_AsMVTGeom(
                {config['geom_column']},
                ST_MakeEnvelope(:min_x, :min_y, :max_x, :max_y, 4326),
                {MVT_TILE_SIZE}, {MVT_TILE_SIZE},
                true, true
            ) AS {config['geom_column']}
        FROM {config['table']}
        WHERE {where_clause})
    """

    return subquery, params


def get_tile_cache_key(z: int, x: int, y: int, layer_name: str = "attractions") -> str:
    """
    Generate a cache key for a specific tile.

    Args:
        z: Zoom level
        x: Tile X coordinate
        y: Tile Y coordinate
        layer_name: Layer name

    Returns:
        Cache key string
    """
    return f"mvt:{layer_name}:{z}:{x}:{y}"


def invalidate_layer_cache(layer_name: str) -> None:
    """
    Invalidate all cached tiles for a specific layer.

    This should be called when heritage/attraction data is updated.

    Args:
        layer_name: Name of the layer to invalidate

    Note:
        Implementation depends on the caching backend (Redis, etc.)
        See Redis caching integration in routes/api/map_routes.py
    """
    logger.info(f"Cache invalidation requested for layer: {layer_name}")
    # Actual implementation in Redis cache handler
