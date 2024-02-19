"""
This should be used for utility aspects only
"""
from django.core.cache import cache
from django.http import JsonResponse

def clear_cache(request) -> None:
    """
    Clears the redis cache
    """
    print(request)
    results = {'error': 'Unable to clear cache'}
    if cache.clear():
        results = {'msg': 'Cache Cleared'}
    return JsonResponse(results)
