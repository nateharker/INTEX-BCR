from django.shortcuts import render
from django.http import HttpResponse
from .models import User

# this is run at the click of a button on choose user type page before getting to the page that allows you to enter credentials
def loginPageView(request) :
    # reset user_id, org_id, and user_type when accessing the login page, or set for the first time
    request.session.flush()
    request.session.clear_expired()
    request.session.set_expiry(0)
    request.session['user_id'] = None
    request.session['org_id'] = None
    request.session['user_type'] = None
    if request.method == 'POST':
        if request.POST.get('usertype') == 'user':
            request.session['user_type'] = 'user'
            return render(request, 'index/login.html')
        elif request.POST.get('usertype') == 'organization':
            request.session['user_type'] = 'org'
            return render(request, 'manlistings/orglogin.html')
        else :
            request.session['user_type'] = 'mentor'
            return render(request, 'manlistings/mentorlogin.html')
    else: 
        return render(request, 'index/login.html')
    

def indexPageView(request) :
    request.session.flush()
    request.session.clear_expired()
    return render(request, 'index/home.html')

def aboutPageView(request) :
    request.session.flush()
    request.session.clear_expired()
    return render(request, 'index/about.html')

def registerPageView(request) :
    # render register form
    return render(request, 'index/register.html')

def createUserPageView(request) :
    # save data to database
    # save username to session storage
    # make sure username entered doesn't already exist
    if (request.method == 'POST') & ((User.objects.filter(username=request.POST.get('username'))).count() < 1) :
        new_user = User()
        new_user.first_name = request.POST.get('first_name')
        new_user.last_name = request.POST.get('last_name')
        new_user.username = request.POST.get('username')
        new_user.email = request.POST.get('email')
        
        new_user.save()
    
    user = User.objects.get(username=request.POST.get('username'))
    request.session['user_id'] = user.id

    context = {
        "user" : user,
        "welcome_message" : "Welcome to your new account!"
    }
    return render(request, 'search/account.html', context)

# this renders the choose user page view
def chooseLoginPageView(request) :
    return render(request, 'index/chooseLogin.html')