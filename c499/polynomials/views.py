from django.shortcuts import render
from django.http import HttpResponse

# Main polynomial landing page?
def index(request):
    return HttpResponse("This is the polynomial!") 

# Add set of integer to new table
def index(request,session_id,set_id):

    return HttpResponse("added new table with integer")


