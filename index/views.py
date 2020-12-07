from django.shortcuts import render
from django.http import HttpResponse
# from .models import _____

def loginPageView(request) :
    return render(request, 'index/login.html')

def indexPageView(request) :
    return render(request, 'index/home.html')

def aboutPageView(request) :
    return render(request, 'index/about.html')

# perhaps instead of typing user in url you can just 
# def userDashPageView(request, person.person_id) :
#     return HttpResponse(person_id)

