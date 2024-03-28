"""
The viewsets for Transactions
"""
from rest_framework import viewsets
#from rest_framework import viewsets, status, filters
#from rest_framework.permissions import IsAuthenticated
#from rest_framework.decorators import action
#from rest_framework.decorators import api_view
#from rest_framework.response import Response

# Create your views here.
class TransactionViewSet(viewsets.ModelViewSet):
    """The Transaction ViewSet that queries the Transaction table

    :param viewsets: The ModelViewSet, so we can access the db
    :type viewsets: class
    :return: Returns the Viewset for stocks
    :rtype: viewset
    """
