from django.shortcuts import render

# Create your views here.
""" 
viewset for setting the rules
"""

import json

from rest_framework.response import Response
from datetime import datetime

from rest_framework import viewsets, status, filters
from rest_framework import filters

from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from rules.models import Rules
from rules.serializers import RuleSerializer
from rest_framework.decorators import action

class RuleViewSet(ModelViewSet):
    """
    The view set for the rules
    """
    kwargs = {}
    serializer_class = RuleSerializer
    queryset = Rules.objects.all().order_by('-id')

    @action(detail=False, methods=['post'])
    def create(self, request):
        """
        endpoint for creating new rules
        """
        try:
            json_body = json.loads(request.body.decode(encoding='utf-8'))
        except Exception:
            return Response(
                {'errors': ['Invalid Request']},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=json_body)
        serializer.is_valid(raise_exception=True)
        rule = serializer.save()

        return Response({'errors': None, 'records': [serializer.data], 'count': len(rule)}, status=status.HTTP_201_CREATED)

    
    

#     #list all rules


#     def set_status(self, status):
#         """
#         setting the rule to inactive (0)
#         """

#         if status not in (0, 1):
#             raise ValueError("Status must be 0 (inactive) or 1 (active).")
#         self.status = status


# # allow to update rule
#     def update_rule(self, rule_name:str, **kwargs):
#         """
#         Update elements of the rule
#         """

#         rule = self.get_rule_by_name(rule_name)
#         if rule:
#             for key, value in kwargs.items():
#                 if hasattr(rule, key):
#                     setattr(rule, key, value)
#                 else:
#                     raise AttributeError(f"Rule has no attribute '{key}'.")
#         else:
#             raise ValueError("Rule not found.")


#     @action(detail=False, methods=['post'], permission_classes=[AllowAny])
#     def get_rule_by_name(self, rule_name: str):
#         """
#         Get rule by name
#         """
        
#         return self.rules.get(rule_name, None)
    

        
        
#     #json object of a python dict
#     @action(detail=False, methods=['post'], permission_classes=[AllowAny])
#     def json_object(self, request):
#         """
#         json object of a python dict
#         """