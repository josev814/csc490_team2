"""
This should be used for utility aspects only
"""
from django.core.cache import cache
from django.http import JsonResponse

def clear_cache(self) -> None:
    """
    Clears the redis cache
    """
    results = {'error': 'Unable to clear cache'}
    if cache.clear():
        results = {'msg': 'Cache Cleared'}
    return JsonResponse(results)

