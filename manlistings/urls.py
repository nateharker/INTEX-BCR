from django.urls import path
from .views import dashIndexPageView

urlpatterns = [
    path("", dashIndexPageView, name="manListDash")    
]