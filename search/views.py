from django.shortcuts import render
from django.http import HttpResponse
# from .models import _____

def indexPageView(request) :
    return render(request, 'search/searchIndex.html')

# perhaps instead of typing user in url you can just 
# def userDashPageView(request, person.person_id) :
#     return HttpResponse(person_id)

