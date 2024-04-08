""" 
Viewset for Rules
"""

from django.http import Http404
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
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        user = self.request.user.id
        parent_qs = super().get_queryset()
        qs = self.filter_queryset(parent_qs).filter(user=user).filter(pk=kwargs.get('pk'))
        if not qs.exists():
            return Response(
                {'errors': ['You do not have permission to delete this rule.']},
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            super().destroy(request, *args, **kwargs)
            return Response(
                {'errors': None, 'message': 'Record Deleted'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Http404:
            return Response(
                {'errors': ['Record Not Found']},
                status=status.HTTP_404_NOT_FOUND
            )

class UpdateAPIView(generics.UpdateAPIView):
    """
    Class for Updating a rule
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RuleSerializer
    queryset = Rules.objects.all()
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        user = self.request.user.id
        parent_qs = super().get_queryset()
        qs = self.filter_queryset(parent_qs).filter(user=user).filter(pk=kwargs.get('pk'))
        if not qs.exists():
            return Response(
                {'errors': ['You do not have permission to update this rule.']},
                status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            super().update(request, *args, **kwargs)
            return Response(
                {'errors': None, 'message': 'Record Updated'},
                status=status.HTTP_200_OK
            )
        except Http404:
            return Response(
                {'errors': ['Record Not Found']},
                status=status.HTTP_404_NOT_FOUND
            )

    def checkout(rule):
        """parsing through the rule logic

        :param rule: 
        :type rule: 
        """

        symbol = rule['ticker']

        # if symbol price > value then perform action
        if rule['condition'] == 'if':
            if symbol[rule['price']] > rule['value']:
                perform(rule['action'])
            
            #continues with condition == 'and' and greater than
            if rule['condition'] == 'and':
                if symbol[rule['price']] > rule['value']:
                    perform(rule['action'])

            #continues with condition == 'and' and less than
            if rule['condition'] == 'and':
                if symbol[rule['price']] < rule['value']:
                    perform(rule['action'])


        # if symbol price < value then perform action
        if rule['condition'] == 'if':
            if symbol[rule['price']] < rule['value']:
                perform(rule['action'])
            
            #continues with condition == 'and' and greater than
            if rule['condition'] == 'and':
                if symbol[rule['price']] > rule['value']:
                    perform(rule['action'])

            #continues with condition == 'and' and less than
            if rule['condition'] == 'and':
                if symbol[rule['price']] < rule['value']:
                    perform(rule['action'])


    def calculate_rule(rule, checkout):
        """function to calculate the action of the rule

        :param rule: _description_
        :type rule: _type_
        :param checkout: _description_
        :type checkout: _type_
        """
        # if method == buy then "amount" needs to go UP by quantity
        if rule['method'] == 'buy':
            amount += rule['quantity']
            
        
        # if method == sell then "amount" needs to go DOWN by quantity
        # this would always sell the available amount of "quantity",
            # but raises an error when "amount" goes below 0 (into the negatives)
        if rule['method'] == 'sell':
            try:
                amount -= rule['quantity']
                if amount < 0:
                    raise ValueError("Selling quantity exceeds available amount.")
            except ValueError as e:
                print(e)
                return 0
