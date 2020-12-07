from index.models import User, JobOffer
from django.shortcuts import render
from django.http import HttpResponse


# make sure the login page can override the key if necessary
def applicantDashPageView(request) :
    if (request.session['user_id'] == None) & (request.POST.get('username') != request.session['user_id']):
        input_username = request.POST.get('username')
        user = User.objects.get(username=input_username)
        if user != None:
            request.session['user_id'] = user.id
        else :
            context = {
                "error_message" : input_username + ' is not a valid username. Please try again.'
            }
            return render(request, 'index/login.html', context)
    else: 
        user = User.objects.get(id=request.session['user_id'])
        job_offers = JobOffer.objects.filter(user_id=request.session['user_id'])
        context = {
            "user" : user,
            "job_offers" : job_offers
        }
        return render(request, 'search/applicantDash.html', context)

def jobOfferPageView(request) :
    return render(request, 'index/login.html')