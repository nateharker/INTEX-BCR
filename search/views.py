from index.models import JobListingSkill, Joblisting, User, JobOffer, Skill
from django.shortcuts import render
from django.http import HttpResponse

# organization recommender with all inputs (simplified to reduce loading times)
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

# organization recommender when we don't have a valid User id (simplified to reduce loading times)
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

# organization recommender for when we don't have an organization id (simplified to reduce loading times)
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

# renders applicant dashboard page if username is valid, also returns job offers for the page. 
# Otherwise, redirects to login page with invalid username error message 
def applicantDashPageView(request) :
    # if submitting login form to get here, store that id in session and display page, otherwise, display the user being used when navigating to page
    if (request.method == 'POST') :
        input_username = request.POST.get('username')
        # if there's a user that matches that username, store it's id in the session and render the applicant dash with context
        try: 
            user = User.objects.get(username=input_username)
            request.session['user_id'] = user.id
        # if no matching objects, let the user know it's an invalid username 
        except: 
            context = {
                "error_message" : input_username + ' is not a valid username. Please try again.'
            }
            return render(request, 'index/login.html', context)
    else: 
        user = User.objects.get(id=request.session['user_id'])
    
    # collect job offers aassociated with user
    job_offers = JobOffer.objects.filter(user_id=request.session['user_id'])
    # if no associated job offers, return string explaining so
    if job_offers.count() < 1 :
        no_offers_message = 'You have no job offers.'
    else : 
        no_offers_message = ''

    #  store the context, and return applicantDash
    context = {
        "user" : user,
        "job_offers" : job_offers,
        'no_offers_message' : no_offers_message,
    }
    return render(request, 'search/applicantDash.html', context)

# show listings that are searched by users
def listingSearchPageView(request) :
    # if getting here through navigation, don't try to collect search terms and just display the page without context
    # if posting a form to get here, it means we have searched something, so collect search terms, store them so we can come back to them, 
    # and find listings where the search terms are inside of the job title
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

# show the side preview of a listing, making available the detail button
def listingPreviewPageView(request) :
    listing_id = request.POST.get('selected_listing_id')
    selected_listing = Joblisting.objects.filter(id=listing_id)
    # redo search so we can have the listing list still
    job_listings = Joblisting.objects.filter(job_title__icontains=request.session['search_terms'])[:50]
    # pass the job_listings list and selected listing
    context = {
        "selected_listings" : selected_listing,
        "job_listings" : job_listings,
        "search_terms" : request.session['search_terms'],
    }
    return render(request, 'search/listingSearchPreview.html', context)

# show the listing details and execute a recommender depending on how much valid info we hav
def listingDetailPageView(request) :    
    # grab the selected listing we are showing details and recommendations for
    listing_id = request.POST.get('selected_listing_id')
    selected_listing = Joblisting.objects.get(id=listing_id)
    userId = int(request.session['user_id'])
    listing_list = []
    organization_list = []
    null_org_message = ""

    # determine if we have a vaild userId and orgId and run a different recommendation accordingly 
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
        # the recommenders return organizations, so choose the top listing from each organization and add that to a list of them
        # if the organization doesn't have any listings, don't give it a card (so we don't have blank listing cards)
        for org_id in organization_list :
            if (Joblisting.objects.filter(organization=org_id)).first() is not None :
                listing_list.append((Joblisting.objects.filter(organization=org_id)).first())

    context = {
        "selected_listing" : selected_listing,
        "listing_list" : listing_list,
        "null_org_message" : null_org_message,
    }
    return render(request, 'search/listingDetail.html', context)

# display job offer detail page with job offer details that are passed through from when a job offer is clicked on applicant dashboard
def offerDetailPageView(request) :
    offer_id = request.POST.get('job_offer_id')
    selected_offer = JobOffer.objects.get(id=offer_id)
    context = {
        "selected_offer" : selected_offer,
    }
    return render(request, 'search/offerDetail.html', context)

# page placeholder for pages that we don't have the time or resources to implement
def underConstructionPageView(request) :
    return render(request, 'search/underConstruction.html')

# display account details and allow updating and deleting of current user
def accountPageView(request) :
    user = User.objects.get(id=request.session['user_id'])
    
    context = {
        "user" : user,
        "welcome_message" : "",
    }
    return render(request, 'search/account.html', context)

# this actually saves the edited fields on the account page and returns the account page again
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

# this view function deletes the active user and redirects to the login page with a deletion message
def deleteUserPageView(request) :
    user_id = request.session['user_id']
    request.session['user_id'] = None
    user = User.objects.filter(id=user_id).delete()
    context = {
        'error_message' : 'User has been deleted.'
    }
    return render(request, 'index/login.html', context)