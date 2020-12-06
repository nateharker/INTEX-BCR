from django.shortcuts import render
from django.http import HttpResponse
# from .models import _____

def indexPageView(request) :
    return HttpResponse('search app index (overall index until we get login in)')

# perhaps instead of typing user in url you can just 
# def userDashPageView(request, person.person_id) :
#     return HttpResponse(person_id)

