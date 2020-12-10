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

    url = 'https://ussouthcentral.services.azureml.net/workspaces/33669fccee6e44bb9fe4cec0e11d2195/services/4beb0953bdf642848bc2b045f9e41422/execute?api-version=2.0&details=true'
    api_key = 'd4//+i9rRZsNJRlDjRvrhv3C6O4zn/RiXE5f/feuvb9Je03fDncCGPdC/80b1p1oyrpc5HBFQMG2wXPfXDBL2A==' 
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

def bcr_similar_companies(orgId) :
  import urllib
  from urllib import request
  import json 

  # insert data into variable in format that Azure ML is expecting
  data =  {
          "Inputs": {

                  "input1":
                  {
                      "ColumnNames": ["organization_id"],
                      "Values": [[ orgId ]]
                  }        
          }
  }
  # assign data to body variable in json format
  body = str.encode(json.dumps(data))

  url = 'https://ussouthcentral.services.azureml.net/workspaces/33669fccee6e44bb9fe4cec0e11d2195/services/c483c64490da49ffadd5205721b6dc59/execute?api-version=2.0&details=true'
  api_key = 'x5FPutHkgx/mExuyneilRTS8PRL5IgTIEJ9HFS1rMah6/3h1HkQQka5e+fLEeXiPET48EXyHLzKmhsT5EW6sMg==' 
  headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
  # format request with url, input previously loaded, and headers - which contains the API key
  req = urllib.request.Request(url, body, headers) 

  response = urllib.request.urlopen(req)
  result = response.read()
  result = json.loads(result)

  # Create array of related organizations
  relatedArray = []
  for iNum in range(0,10) :
    relatedArray.append(int(result['Results']['output1']['value']['Values'][0][iNum]))

  return relatedArray      

def bcr_org_recom_simp(userId) :
  import urllib
  from urllib import request
  import json 
  
  # insert data into variable in format that Azure ML is expecting 
  data =  {
          "Inputs": {

                  "input1":
                  {
                      "ColumnNames": ["user_id"],
                      "Values": [[ userId ]]
                  }        
          }
  }
  # assign data to body variable in json format
  body = str.encode(json.dumps(data))

  url = 'https://ussouthcentral.services.azureml.net/workspaces/33669fccee6e44bb9fe4cec0e11d2195/services/762f03f941b14ec18fd4ff574d969281/execute?api-version=2.0&details=true'
  api_key = 'FcKbi+rABUqHwyqeboIwlM+yHmfGs3sbe4LwtfWgcaITmJPItPaumZOC1P/z2h0ZeUojUWcG/mPNxufg548ywg==' 
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
        # filters to see if the job title contains the search terms
        job_listings = Joblisting.objects.filter(job_title__icontains=search_terms)[:50]
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
    job_listings = Joblisting.objects.filter(job_title__icontains=request.session['search_terms'])[:50]
    context = {
        "selected_listings" : selected_listing,
        "job_listings" : job_listings,
        "search_terms" : request.session['search_terms'],
    }
    return render(request, 'search/listingSearchPreview.html', context)


def listingDetailPageView(request) :    
    listing_id = request.POST.get('selected_listing_id')
    selected_listing = Joblisting.objects.get(id=listing_id)
    userId = int(request.session['user_id'])
    listing_list = []
    organization_list = []
    null_org_message = ""

    if (selected_listing.organization is None) and ((userId > 201) or (userId < 2)):
        null_org_message = "We don't have enough information to make a recommendation."
    else : 
        if (selected_listing.organization is None) :
            organization_list = bcr_org_recom_simp(userId)
        else :
            orgId = selected_listing.organization.id
            if (userId > 201) or (userId < 2):
                organization_list = bcr_similar_companies(orgId)
            else : 
                organization_list = bcr_org_recommender(userId, orgId)

        for org_id in organization_list :
            if (Joblisting.objects.filter(organization=org_id)).first() is not None :
                listing_list.append((Joblisting.objects.filter(organization=org_id)).first())

    # test_listing = (Joblisting.objects.filter(organization=organization_list[0])).first()
    # implement if we extra time
    # listing_skills = JobListingSkill.objects.filter(job_listing=listing_id)
    # skill_descriptions = Skill.objects.filter(id=listing_skills.skill)

    context = {
        "selected_listing" : selected_listing,
        "listing_list" : listing_list,
        "null_org_message" : null_org_message,
        # "test_listing" : test_listing,
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
        "user" : user,
        "welcome_message" : "",
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

def deleteUserPageView(request) :
    user_id = request.session['user_id']
    request.session['user_id'] = None
    user = User.objects.filter(id=user_id).delete()
    context = {
        'error_message' : 'User has been deleted.'
    }
    return render(request, 'index/login.html', context)