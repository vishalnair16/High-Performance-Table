import json
import logging
from typing import Optional, Any
from app.core.config import settings
import redis.asyncio as redis
from datetime import timedelta

logger = logging.getLogger(__name__)

class Cache:
    redis_client: Optional[redis.Redis] = None

cache = Cache()

async def connect_to_redis():
    """Create Redis connection"""
    try:
        if not settings.ENABLE_CACHE:
            logger.info("⚠️  Caching is disabled")
            return
        
        # Build connection URL
        redis_url = f"redis://"
        if settings.REDIS_PASSWORD:
            redis_url = f"redis://:{settings.REDIS_PASSWORD}@"
        redis_url += f"{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
            
        cache.redis_client = redis.from_url(
            redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=50,
        )
        
        # Test connection
        await cache.redis_client.ping()
        logger.info("✅ Connected to Redis!")
    except Exception as e:
        logger.warning(f"⚠️  Redis connection failed (continuing without cache): {e}")
        cache.redis_client = None

async def close_redis_connection():
    """Close Redis connection"""
    if cache.redis_client:
        await cache.redis_client.aclose()
        logger.info("✅ Disconnected from Redis")

async def get_cache(key: str) -> Optional[Any]:
    """Get value from cache"""
    if not cache.redis_client or not settings.ENABLE_CACHE:
        return None
    
    try:
        value = await cache.redis_client.get(key)
        if value:
            return json.loads(value)
    except Exception as e:
        logger.warning(f"Cache get error: {e}")
    return None

async def set_cache(key: str, value: Any, ttl: Optional[int] = None):
    """Set value in cache"""
    if not cache.redis_client or not settings.ENABLE_CACHE:
        return
    
    try:
        ttl = ttl or settings.CACHE_TTL
        await cache.redis_client.setex(
            key,
            ttl,
            json.dumps(value, default=str)
        )
    except Exception as e:
        logger.warning(f"Cache set error: {e}")

async def delete_cache(key: str):
    """Delete key from cache"""
    if not cache.redis_client or not settings.ENABLE_CACHE:
        return
    
    try:
        await cache.redis_client.delete(key)
    except Exception as e:
        logger.warning(f"Cache delete error: {e}")

async def delete_cache_pattern(pattern: str):
    """Delete all keys matching pattern"""
    if not cache.redis_client or not settings.ENABLE_CACHE:
        return
    
    try:
        keys = await cache.redis_client.keys(pattern)
        if keys:
            await cache.redis_client.delete(*keys)
    except Exception as e:
        logger.warning(f"Cache pattern delete error: {e}")

def generate_cache_key(endpoint: str, **kwargs) -> str:
    """Generate cache key from endpoint and parameters"""
    params = "_".join(f"{k}_{v}" for k, v in sorted(kwargs.items()) if v is not None)
    return f"cache:{endpoint}:{params}"

