"""
Custom Pagination Classes
"""
from rest_framework import status, pagination
from rest_framework.response import Response

class PaginationWithLinks(pagination.PageNumberPagination):
    """
    Custom pagination class listing rules
    """
    def get_paginated_response(self, data):
        return Response({
            'errors': None,
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'records': data
        }, status=status.HTTP_200_OK)
