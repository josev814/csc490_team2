"""
Holds the business logic for the application
"""
#from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    """
    The default endpoint
    """
    print(request)
    return HttpResponse("Hello, world. The index of analysts")
