"""
This should be used for utility aspects only
"""
from django.core.cache import cache
from rest_framework.response import Response

def clear_cache(request) -> None:
    """
    Clears the redis cache
    """
    print(request)
    results = {'errors': ['Unable to clear cache']}
    if cache.clear():
        results = {'msg': 'Cache Cleared', 'errors': None}
    return Response(results)
