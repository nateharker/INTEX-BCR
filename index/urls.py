from django.urls import path
from .views import indexPageView, aboutPageView, chooseLoginPageView, loginPageView, registerPageView, createUserPageView

urlpatterns = [
    path('chooselogin/', chooseLoginPageView, name='chooselogin'),
    path('login/', loginPageView, name='login'),
    path('about/', aboutPageView, name='about'),
    path('register/', registerPageView, name='register'),
    path('createuser/', createUserPageView, name='createuser'),


    path('', indexPageView, name='index'),
    
    
]
