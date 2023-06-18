from django.urls import path
from . import views



urlpatterns= [
    
    path("",views.home,name="home-page"),
    
    # localhost/signup that will display the views from signup function
    # the name is used to be able to be called at the html file
    path("signup", views.signup, name="signup"),
    
    #we need to add/<int:pk whenever we received a private key(pk) 
    path("profile/<int:pk>/", views.profile, name="profile"),
    
  
    
    
    
]