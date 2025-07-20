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


import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

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
        r = get_redis_connection("default")
        info = r.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        if total_requests > 0:
            hit_ratio = hits / total_requests
        else:
            hit_ratio = 0  # or None, depending on your requirement

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

