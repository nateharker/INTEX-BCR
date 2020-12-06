from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def dashIndexPageView(request) :
    return HttpResponse('Manlistings app Dashboard')