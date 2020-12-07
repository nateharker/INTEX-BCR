from django.urls import path
from .views import indexPageView, aboutPageView, applicantDashPageView

urlpatterns = [
    path("", indexPageView, name="index"),
    path("about/", aboutPageView, name="about"),
    path("applicantdash/", applicantDashPageView, name="applicantdash"),
    
    #  path("<int:{{ user_id }}>/", userDashPageView, name="use dash"),  MAYBE DO SOMETHING LIKE THIS FOR USER LOGIN
                                            # Just need a way to specify the user_id that would be there
]
