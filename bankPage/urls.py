from django.urls import path
from . import views



urlpatterns= [
    
    path("",views.home,name="home-page"),
    
    # localhost/signup that will display the views from signup function
    # the name is used to be able to be called at the html file
    path("signup", views.signup, name="signup"),
    
    
    path("profile", views.profile, name="profile"),
    
    path("cashin", views.cashin, name="cashin"),
    path("cashout", views.cashout, name="cashout"),
    path("history", views.history, name="history"),
    path("navbar",views.navbar,name="navbar"),
    path("transfer",views.transfer,name="transfer"),
    path("confirmation",views.confirmation,name="confirmations"),
    
    
    
    
  
    
    
    
]