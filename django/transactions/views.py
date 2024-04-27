"""
The viewsets for Transactions
"""
from rest_framework import generics, status, pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Transactions
from .serializer import TransactionSerializer

class CustomLimitPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 1000

# Create your views here.
class ListRuleTransactionsAPIView(generics.ListAPIView):
    """
    Queries the Transaction table for a specific rule id and returns the results
    """
    permission_classes = (IsAuthenticated,)
    queryset = Transactions.objects.all().order_by('-timestamp', '-pk')
    serializer_class = TransactionSerializer
    lookup_field = 'pk'
    pagination_class = CustomLimitPagination
        
    def list(self, request, *args, **kwargs):
        rule = kwargs['rule']
        parent_qs = self.get_queryset()
        qs = self.filter_queryset(parent_qs).filter(rule=rule)
        if not qs.exists():
            return Response(
                {'errors': ['No Transactions found']},
                status=status.HTTP_404_NOT_FOUND
            )
        
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(qs, many=True)
        data = serializer.data
        return Response(
            {
                'errors': None,
                'records': data,
                'count': len(data)
            },
            status = status.HTTP_200_OK
        )

class GetAPIView(generics.RetrieveAPIView):
    """
    Gets a specific transaction
    """
    permission_classes = (IsAuthenticated,)
    queryset = Transactions.objects.all().order_by('-timestamp').order_by('-pk').all()
    serializer_class = TransactionSerializer
    lookup_field = 'pk'
