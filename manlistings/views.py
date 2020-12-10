from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from index.models import User, JobOffer, Joblisting, Organization

# recommends applicants to organization based on user being viewed and organization doing the viewing
def bcr_app_recommender(orgId, userId) :
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

  url = 'https://ussouthcentral.services.azureml.net/workspaces/33669fccee6e44bb9fe4cec0e11d2195/services/34e37131876d4dc59a1585a96a4ba6fe/execute?api-version=2.0&details=true'
  api_key = 'Hll/9GyszQvzZ9aZqQVuFOk5QZIEVHpD3yXbVe3P+K1RVpBEYi1JwBgfPuL3VVdhyK+RtiwQN+vO4/RMRaMZeA==' 
  headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
  # format request with url, input previously loaded, and headers - which contains the API key
  req = urllib.request.Request(url, body, headers) 

  response = urllib.request.urlopen(req)
  result = response.read()
  result = json.loads(result)

  # Create array of applicant recommendations
  appArray = []
  for iNum in range(0,10) :
    appArray.append(int(result['Results']['output1']['value']['Values'][0][iNum]))

  return appArray

# displays organization dashboard view based on organization logging in or currently logged in 
def organizationDashPageView(request) :
    # Only request to this page is login, so if they are logging in it will get the username, otherwise it will use org_id stored
    if (request.method == 'POST') :
        input_email = request.POST.get('email')
        # if there's a user that matches that username, store it's id, else, let the user know it's an invalid username 
        try: 
            user = Organization.objects.get(email=input_email)
            request.session['org_id'] = user.id
        except :
            context = {
                "error_message" : input_email + ' is not a valid email. Please try again.'
            }
            return render(request, 'manlistings/orglogin.html', context)
    else: 
        user = Organization.objects.get(id=request.session['org_id'])
    
    # collect job offers aassociated with user, store the context, and return orgdash
    job_listings = Joblisting.objects.filter(organization=request.session['org_id'])
    # if no associated job offers, return string explaining so, else leave string blank
    if job_listings.count() < 1 :
        no_listings_message = "You haven't posted any job listings."
    else :
        no_listings_message = ''
    context = {
        "user" : user,
        "job_listings" : job_listings,
        'no_listings_message' : no_listings_message,
    }
    return render(request, 'manlistings/orgdash.html', context)

# display user search page view
def userSearchPageView(request) :
    # check if we are searching. If so, pull search terms, if not, just display the template without context
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # if null values in search, assign with a string that won't return any names in our query (otherwise we'd get every name returned)
        if not first_name:
            first_name = str(1)
        if not last_name:
            last_name = str(1)
        # filters to look for first and last name in search string
        applicants = User.objects.filter(Q(first_name__icontains=first_name) | Q(last_name__icontains=last_name))[:50]
        # if no job listings, return string explaining so, else leave string blank
        if applicants.count() < 1 :
            # reassign the search terms to what they actually were so that the error message displays correctly
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            no_listings_message = 'There are no applicants named ' + first_name + ' ' + last_name
        else :
            no_listings_message = ''
        # pass through the users that returned from the search
        context = {
            "applicants" : applicants,
            'no_listings_message' : no_listings_message,
        }
        return render(request, 'manlistings/userSearch.html', context)
    else :
        return render(request, 'manlistings/userSearch.html')

# show user details along with machine learning recommendations for other users based on the userID and organization id
def userDetailPageView(request) :
    # collect the user and organization info we need
    userId = int(request.POST.get('user_id'))
    selected_user = User.objects.get(id=userId)
    orgId = request.session['org_id']
    user_id_list = []
    null_user_list_message = ""

    # if it's a valid user id we can use, run the recommender, otherwise return an error message
    if int(userId) > 201:
        null_user_list_message = "We don't have enough information about this user to provide recommendations!"
    else :
        user_id_list = bcr_app_recommender(userId, orgId)

    # append the users that coincide with the id list to a user list that we will then pass through
    recommended_user_list =[]
    for user_id in user_id_list :
        recommended_user_list.append((User.objects.get(id=user_id)))

    context = {
        "selected_user" : selected_user,
        "recommended_user_list" : recommended_user_list,
        "null_user_list_message" : null_user_list_message,
    }
    return render(request, 'manlistings/userDetail.html', context)

# return basic listing detail page to show more details on the organizations own listings (without showing a recommender)
def simpListingDetailPageView(request) :
    listing_id = request.POST.get('selected_listing_id')
    selected_listing = Joblisting.objects.get(id=listing_id)
    
    context = {
        "selected_listing" : selected_listing,
    }
    return render(request, 'manlistings/simplistdet.html', context)

# show the organization's account details
def orgAccountPageView(request) :
    org = Organization.objects.get(id=request.session['org_id'])
    
    context = {
        "org" : org,
    }
    return render(request, 'manlistings/orgAccount.html', context)

# page placeholder for pages that we didn't have the time or resources to create (beyond the scope of this prototype)
def orgUnderConstructionPageView(request) :
    return render(request, 'manlistings/orgMessages.html')