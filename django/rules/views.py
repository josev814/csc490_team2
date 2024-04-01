""" 
Viewset for Rules
"""

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Rules
from .serializers import RuleSerializer



class CreateAPIView(generics.CreateAPIView):
    """
    Class for Creating a rule
    """
    permission_classes = (IsAuthenticated,)
    queryset = Rules.objects.all()
    serializer_class = RuleSerializer

    def perform_create(self, serializer):
        """
        Overriding the default perform_create so we can assign the user
        Creates a rule for a user
        """
        user = self.request.user
        serializer.save(user=user)


class ListAPIView(generics.ListAPIView):
    """
    API Endpoint for listing rules for a user
    """
    permission_classes = (IsAuthenticated,)
    queryset = Rules.objects.order_by('-pk').all()
    serializer_class = RuleSerializer

    def list(self, request, *args, **kwargs):
        """
        Overriding the default list so we can reformat the Response
        Lists the rules for an authenticated user
        """
        print(request)
        user = self.request.user
        parent_qs = super().get_queryset(*args, **kwargs)
        qs = self.filter_queryset(parent_qs).filter(user=user)
        if not qs.exists():
            return Response(
                {'errors': ['No rules found for the user']},
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
            status=status.HTTP_200_OK
        )
        

class DetailAPIView(generics.RetrieveAPIView):
    """
    API View to list details for a specific rule
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RuleSerializer
    queryset = Rules.objects.all()
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        """
        Overriding the default retrieval so we can reformat the Response
        """
        print(request)
        print(args)
        print(kwargs)
        instance = self.get_object()
        if instance is None:
            return Response(
                {'errors': ['Record does not exist']},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(instance)
        return Response(
            {'errors': None, 'record': serializer.data},
            status=status.HTTP_200_OK
        )

class DeleteAPIView(generics.DestroyAPIView):
    """
    Class for Deleting a rule
    """
    permission_classes = (IsAuthenticated,)
    queryset = Rules.objects.all()
    serializer_class = RuleSerializer
    lookup_field = "id"

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {'errors': None, 'message': 'Record Deleted'},
            status=status.HTTP_204_NO_CONTENT
        )
    