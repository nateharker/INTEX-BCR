from django.shortcuts import render
from django.http import HttpResponse
# from .models import _____

def indexPageView(request) :
    return render(request, 'search/searchIndex.html')

def aboutPageView(request) :
    return render(request, 'search/about.html')

def applicantDashPageView(request) :
    data = 'test' #get relevant user object based on ID stored somewhere?

    context = {
        "user" : data
    }

    return render(request, 'search/applicantDash.html', context)

# perhaps instead of typing user in url you can just 
# def userDashPageView(request, person.person_id) :
#     return HttpResponse(person_id)

