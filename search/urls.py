from django.urls import path
from .views import applicantDashPageView, listingSearchPageView, listingPreviewPageView, listingDetailPageView, underConstructionPageView, accountPageView, offerDetailPageView, saveUserInfoPageView

urlpatterns = [
    path("applicantdash", applicantDashPageView, name="applicantdash"),
    path("listingsearch", listingSearchPageView, name="listingsearch"),
    path("listingsearch/preview", listingPreviewPageView, name="listingpreview"),
    path("listingdetail", listingDetailPageView, name="listingdetail"),
    path("offerdetail", offerDetailPageView, name="offerdetail"),
    path("account", accountPageView, name="account"),
    path("saveuser", saveUserInfoPageView, name="saveuser"),
    
    path("underconstruction", underConstructionPageView, name="underconstruction"),
]
