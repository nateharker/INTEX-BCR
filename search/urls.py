from django.urls import path
from .views import applicantDashPageView, listingSearchPageView, listingPreviewPageView, listingDetailPageView, underConstructionPageView, offerDetailPageView 
from .views import saveUserInfoPageView, deleteUserPageView, accountPageView

urlpatterns = [
    path("applicantdash", applicantDashPageView, name="applicantdash"),
    path("listingsearch", listingSearchPageView, name="listingsearch"),
    path("listingsearch/preview", listingPreviewPageView, name="listingpreview"),
    path("listingdetail", listingDetailPageView, name="listingdetail"),
    path("offerdetail", offerDetailPageView, name="offerdetail"),
    path("account", accountPageView, name="account"),
    path("saveuser", saveUserInfoPageView, name="saveuser"),
    path("deleteuser", deleteUserPageView, name="deleteuser"),

    path("underconstruction", underConstructionPageView, name="underconstruction"),
]
