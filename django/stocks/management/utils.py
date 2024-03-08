"""
This should be used for utility aspects only
"""
import logging
from rest_framework.response import Response
from django.core.cache import cache

def clear_cache(request) -> None:
    """
    Clears the redis cache
    """
    logging.info(f'clear_cache request: {request}')
    results = {'errors': ['Unable to clear cache']}
    if cache.clear():
        results = {'msg': 'Cache Cleared', 'errors': None}
    return Response(results)
