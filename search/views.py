from index.models import JobListingSkill, Joblisting, User, JobOffer, Skill
from django.shortcuts import render
from django.http import HttpResponse

# organization recommender
def bcr_org_recommender(userId, orgId) :
    import urllib
    from urllib import request
    import json 

    # insert data into variable in format that Azure ML is expecting 
    data =  {
            "Inputs": {

                    "input1":
                    {
                        "ColumnNames": ["user_id", "organization_id"],
                        "Values": [[ userId, orgId ]]
                    }        
            }
    }
    # assign data to body variable in json format
    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/33669fccee6e44bb9fe4cec0e11d2195/services/1065068c292c49c2bd0f948e1368f247/execute?api-version=2.0&details=true'
    api_key = 's44evHm/HrvpoI6tEgSt9taq9IW/idLz9/Q7uFCCd27X1i/YwFII/BplU7+DhlDavUHMQyDG/GZFrjxJjN7Uug==' 
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    # format request with url, input previously loaded, and headers - which contains the API key
    req = urllib.request.Request(url, body, headers) 

    response = urllib.request.urlopen(req)
    result = response.read()
    result = json.loads(result)
    # Create array of organization recommendations
    orgArray = []
    for iNum in range(0,10) :
        orgArray.append(int(result['Results']['output1']['value']['Values'][0][iNum]))
    return orgArray



# make sure the login page can override the key if necessary
def applicantDashPageView(request) :
    # if there's no user saved, OR the user in the username form doesn't match the user saved, then get the new username, else reassign the user to be the saved one
    if (request.session['user_id'] == None) :
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
    
    if request.method == 'POST':
        search_terms = request.POST.get('search_terms')
        request.session['search_terms'] = search_terms
        job_listings = Joblisting.objects.filter(job_title=search_terms)
        # if no job listings, return string explaining so, else leave string blank
        if job_listings.count() < 1 :
            no_listings_message = 'There are no listings titled ' + search_terms
        else :
            no_listings_message = ''
        context = {
            "job_listings" : job_listings,
            'no_listings_message' : no_listings_message,
            "search_terms" : search_terms,
        }
        return render(request, 'search/listingSearch.html', context)
    else :
        return render(request, 'search/listingSearch.html')

def listingPreviewPageView(request) :
    listing_id = request.POST.get('selected_listing_id')
    selected_listing = Joblisting.objects.filter(id=listing_id)
    job_listings = Joblisting.objects.filter(job_title=request.session['search_terms'])
    context = {
        "selected_listings" : selected_listing,
        "job_listings" : job_listings,
        "search_terms" : request.session['search_terms'],
    }
    return render(request, 'search/listingSearchPreview.html', context)


def listingDetailPageView(request) :
    listing_id = request.POST.get('selected_listing_id')
    selected_listing = Joblisting.objects.get(id=listing_id)
    userId = request.session['user_id']
    orgId = selected_listing.organization.id
    listing_list = []
    null_org_message = ""

    if orgId is None :
        null_org_message = "This job listing doesn't have an associated organization to base our recommendations on."
    else : 
        organization_list = bcr_org_recommender(userId, orgId)
        for listing in listing_list :
            listing[0] = Joblisting.objects.filter(organization=organization_list[0]).order_by('?').first()

    # implement if we extra time
    # listing_skills = JobListingSkill.objects.filter(job_listing=listing_id)
    # skill_descriptions = Skill.objects.filter(id=listing_skills.skill)
    context = {
        "selected_listing" : selected_listing,
        "listing_list" : listing_list,
        "null_org_message" : null_org_message,
        # "listing_skills" : listing_skills,
        # "skill_descriptions" : skill_descriptions,
    }
    return render(request, 'search/listingDetail.html', context)

def offerDetailPageView(request) :
    offer_id = request.POST.get('job_offer_id')
    selected_offer = JobOffer.objects.get(id=offer_id)
    context = {
        "selected_offer" : selected_offer,
    }
    return render(request, 'search/offerDetail.html', context)



def underConstructionPageView(request) :
    return render(request, 'search/underConstruction.html')

def accountPageView(request) :
    user = User.objects.get(id=request.session['user_id'])
    context = {
        "user" : user
    }
    return render(request, 'search/account.html', context)

def saveUserInfoPageView(request) :
    user = User.objects.get(id=request.session['user_id'])
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.username = request.POST.get('username')
    user.email = request.POST.get('email')
    user.save()

    context = {
        "user" : user
    }
    return render(request, 'search/account.html', context)