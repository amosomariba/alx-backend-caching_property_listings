from django.core.cache import cache
from .models import Property
import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)


def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        cache.set('all_properties', properties, timeout=3600)
    return properties


def get_redis_cache_metrics():
    """
    Return Redis keyspace hit/miss metrics and hit ratio.

    Returns:
        dict: {
            "hits": int,
            "misses": int,
            "hit_ratio": float | None,
        }
    """
    try:
        # Use the same cache alias you configured in settings (default)
        r = get_redis_connection("default")

        info = r.info()  # full INFO dictionary from Redis
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        total = hits + misses
        hit_ratio = (hits / total) if total > 0 else None

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio,
        }

        logger.info("Redis cache metrics: %s", metrics)
        return metrics

    except Exception as e:
        logger.exception("Failed to retrieve Redis cache metrics: %s", e)
        return {
            "hits": None,
            "misses": None,
            "hit_ratio": None,
            "error": str(e),
        }



