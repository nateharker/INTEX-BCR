from django.urls import path
from .views import organizationDashPageView, userSearchPageView, orgAccountPageView, userDetailPageView, orgUnderConstructionPageView, simpListingDetailPageView

urlpatterns = [
    path("orgdash/", organizationDashPageView, name="orgdash"),
    path("usersearch/", userSearchPageView, name="usersearch"),
    path("userdetail/", userDetailPageView, name="userdetail"),
    path("orgaccount/", orgAccountPageView, name="orgaccount"),
    path("orgunderconstruction/", orgUnderConstructionPageView, name="orgunderconstruction"),
    path("orglistdet/", simpListingDetailPageView, name='simplistdet')

    
    
]