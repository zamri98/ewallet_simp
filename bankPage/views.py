from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from .forms import Userform
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def home(request):
    if request.method == "POST":
        
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user= authenticate(request,username=username,password=password)
    
        if user is not None:
            login(request,user)
        
            
            ### we need for use for futher used of user id
            user_id = user.id
            request.session['user_id'] = user_id
            return redirect('profile')
        else:
            return redirect('home-page')
        
    else:
        return render(request,"main.html",{})

def signup(request):
    
    #if the request method is POST or GET request
    if request.method == "POST":
        
        #sent all the data from the form to be posted into userform in form.py file 
        form =Userform(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            messages.success(request,("There is error in your form"))
            return render(request,"sign.html")
            
        messages.success(request,("Your Account has been Created Succesfully"))
        return redirect('home-page')
        
       
    else:
        return render(request,"sign.html",{})
    
    
def profile(request):
    
    
    user_pk= request.session.get('user_id')
    
    user=User.objects.get(id=user_pk)
    username=user.username
    
    user_balance=Balance.objects.get(user_id=user_pk)    
        
    return render(request,'profile.html',context={"username":username,"Balance":user_balance.total_balance})
    

def cashin(request):
    
    user_pk= request.session.get('user_id')
    
    return render(request,"cash_in.html")


def cashout(request):
    
    user_pk= request.session.get('user_id')
    
    return render(request,"cash_out.html")
 
        
   

    
    



