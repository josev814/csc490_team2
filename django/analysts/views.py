"""
Holds the business logic for the application
"""
import logging
#from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    """
    The default endpoint
    """
    logging.debug(f'Analysts index: {request}')
    return HttpResponse("Hello, world. The index of analysts")
