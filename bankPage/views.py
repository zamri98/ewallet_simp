from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,"main.html")

def signup(request):
    
    return render(request,"test.html")
