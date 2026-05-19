import json
import logging
from typing import Any, Optional
from flask import current_app

logger = logging.getLogger(__name__)

def cache_get(key: str) -> Optional[Any]:
    """
    Retrieve and deserialize data from Redis cache.
    
    Args:
        key: The cache key to lookup
        
    Returns:
        The deserialized data (dict, list, etc.) or None if miss/error
    """
    redis = getattr(current_app, "redis_client", None)
    if not redis:
        return None
        
    try:
        data = redis.get(key)
        if data:
            logger.debug(f"Cache HIT: {key}")
            # upstash-redis might return bytes or string depending on version/config
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            return json.loads(data)
        
        logger.debug(f"Cache MISS: {key}")
        return None
    except Exception as e:
        logger.error(f"Cache GET error for key '{key}': {e}")
        return None

def cache_set(key: str, data: Any, ttl: int = 3600) -> bool:
    """
    Serialize and store data in Redis cache with a TTL.
    
    Args:
        key: The cache key
        data: The data to store (must be JSON serializable)
        ttl: Time to live in seconds (default: 1 hour)
        
    Returns:
        True if successful, False otherwise
    """
    redis = getattr(current_app, "redis_client", None)
    if not redis:
        return False
        
    try:
        serialized = json.dumps(data)
        # upstash-redis uses 'ex' for TTL in seconds
        redis.set(key, serialized, ex=ttl)
        logger.debug(f"Cache SET: {key} (TTL: {ttl}s)")
        return True
    except Exception as e:
        logger.error(f"Cache SET error for key '{key}': {e}")
        return False

def cache_delete(key: str) -> bool:
    """
    Delete a key from Redis cache.
    
    Args:
        key: The cache key to delete
        
    Returns:
        True if successful, False otherwise
    """
    redis = getattr(current_app, "redis_client", None)
    if not redis:
        return False
        
    try:
        redis.delete(key)
        logger.debug(f"Cache DELETE: {key}")
        return True
    except Exception as e:
        logger.error(f"Cache DELETE error for key '{key}': {e}")
        return False

def cache_invalidate_pattern(pattern: str) -> int:
    """
    Invalidate multiple keys matching a pattern.
    NOTE: Pattern matching can be expensive on large datasets.
    
    Args:
        pattern: The glob pattern (e.g., "mvt:attractions:*")
        
    Returns:
        Number of keys deleted
    """
    redis = getattr(current_app, "redis_client", None)
    if not redis:
        return 0
        
    try:
        keys = redis.keys(pattern)
        if keys:
            redis.delete(*keys)
            logger.info(f"Cache PATTERN DELETE: {pattern} ({len(keys)} keys)")
            return len(keys)
        return 0
    except Exception as e:
        logger.error(f"Cache PATTERN DELETE error for '{pattern}': {e}")
        return 0

def invalidate_attraction_cache(attraction_id: Optional[int] = None, barangay_id: Optional[int] = None):
    """
    Centralized helper to invalidate all caches related to attractions.
    Should be called on add, edit, delete, or approval.
    """
    # Global/Shared caches
    cache_delete("home_featured_attractions")
    cache_delete("map_page_meta")
    cache_invalidate_pattern("api_attractions:*")
    
    # Specific caches
    if attraction_id:
        cache_delete(f"attraction_detail_v1:{attraction_id}")
    
    if barangay_id:
        cache_delete(f"barangay_data:{barangay_id}")
        # Also clear by name if we can resolve it, but ID is primary for data payload
        
def invalidate_event_cache(event_id: Optional[int] = None, barangay_id: Optional[int] = None):
    """
    Centralized helper to invalidate all caches related to events.
    """
    # Events currently affect search results and barangay profiles
    cache_invalidate_pattern("search:*")
    
    if barangay_id:
        cache_delete(f"barangay_data:{barangay_id}")

def invalidate_business_cache(establishment_id: Optional[int] = None, barangay_id: Optional[int] = None):
    """
    Centralized helper to invalidate all caches related to businesses/establishments.
    """
    cache_delete("home_featured_establishments_v2")
    cache_invalidate_pattern("api_establishments:*")
    cache_invalidate_pattern("search:*")
    
    if establishment_id:
        cache_delete(f"establishment_detail_module:{establishment_id}")
        cache_delete(f"establishment_detail_v1:{establishment_id}")
        
    if barangay_id:
        cache_delete(f"barangay_data:{barangay_id}")

