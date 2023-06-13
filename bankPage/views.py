from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    return render(request,"main.html")

def signup(request):
    
    return render(request,"test.html")

def homeProfile(request):
    
    
    profile = Balance.objects.get(id=1)
    
    
    return render(request,"profile.html",{"all_profile":profile})