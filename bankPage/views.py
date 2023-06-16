from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from .forms import Userform
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request,"main.html")

def signup(request):
    
    return render(request,"sign.html")

def homeProfile(request):
    
    
    profile = Balance.objects.get(id=1)
    
    
    return render(request,"profile.html",{"all_profile":profile})

def join(request) :
    
    #if the request method is POST or GET request
    if request.method == "POST":
        
        #sent all the data from the form to be posted into userform in form.py file 
        form =Userform(request.POST or None)
        if form.is_valid():
            form.save()
        messages.add_message()
        return redirect('home')
        
    else:
        return render(request,"join.html")

