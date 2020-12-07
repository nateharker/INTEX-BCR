from index.models import User, JobOffer
from django.shortcuts import render
from django.http import HttpResponse


# make sure the login page can override the key if necessary
def applicantDashPageView(request) :
    # if there's no user saved, OR the user in the username form doesn't match the user saved, then get the new username, else reassign the user to be the saved one
    if (request.session['user_id'] == None) or (request.POST.get('username') != User.objects.get(id=request.session['user_id']).username):
        input_username = request.POST.get('username')
        user = User.objects.filter(username=input_username)
        # if there's a user that matches that username, store it's id, else, let the user know it's an invalid username 
        if user.count() > 0:
            user = user.first()
            request.session['user_id'] = user.id
        else :
            context = {
                "error_message" : input_username + ' is not a valid username. Please try again.'
            }
            return render(request, 'index/login.html', context)
    else: 
        user = User.objects.get(id=request.session['user_id'])
    
    # collect job offers aassociated with user, store the context, and return applicantDash
    job_offers = JobOffer.objects.filter(user_id=request.session['user_id'])
    # if no associated job offers, return string explaining so, else leave string blank
    if job_offers.count() < 1 :
        no_offers_message = 'You have no job offers.'
    else :
        no_offers_message = ''
    context = {
        "user" : user,
        "job_offers" : job_offers,
        'no_offers_message' : no_offers_message,
    }
    return render(request, 'search/applicantDash.html', context)

def jobOfferPageView(request) :
    return render(request, 'index/login.html')

def listingSearchPageView(request) :
    return render(request, 'search/listingSearch.html')