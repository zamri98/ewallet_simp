from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from .forms import Userform,TranscForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from decimal import Decimal
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
    
"""
def cashin(request):
    
    user_pk= request.session.get('user_id')
    user_balance=Balance.objects.get(user_id=user_pk)
    
    if request.method == "POST":
        
        #sent all the data from the form to be posted into TranscForm in form.py file 
        form =TranscForm(request.POST or None)
        if form.is_valid():
            
            #Save the new balance
            clean_data=form.cleaned_data
            new_balance=user_balance.total_balance + Decimal(clean_data["Transaction"])
            user_balance.total_balance =new_balance
            user_balance.save() 
            
            
            
            
           
            form.save()
            #save the type of transaction
            type_value=Transaction.objects.get(user_id=user_pk)
            type_value.transacation_type= "cashin"
            type_value.save()
            messages.success(request,("You Successfull cash in "))
            return redirect('profile')
    
        else:
            messages.success(request,("There is error in your form"))
            return redirect("cashin")
            

    
    else:
        return render(request,"cash_in.html")
"""


def cashin(request):
    user_pk = request.session.get('user_id')
    user_balance = Balance.objects.get(user_id=user_pk)

    if request.method == "POST":
        form = TranscForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            transcation_amount = Decimal(clean_data.get('Transaction'))

            # Update the user's balance
            new_balance = user_balance.total_balance + transcation_amount
            user_balance.total_balance = new_balance
            user_balance.save()

            # Save the transaction with the cash-in type
            
            #we commit to false because we want to add all field first in the form we only provide 2 fields
            #the transaction type not yet
            transaction = form.save(commit=False)
            transaction.user_id = user_pk  # Set the user_id field
            transaction.transacation_type = "cashin"
            transaction.save()

            messages.success(request, "You have successfully cashed in.")
            return redirect('profile')
        else:
            messages.error(request, "There is an error in your form.")
            return redirect('cashin')
    else:
        form = TranscForm()

    return render(request, "cash_in.html", {'form': form})

def cashout(request):
    
    user_pk = request.session.get('user_id')
    user_balance = Balance.objects.get(user_id=user_pk)
    
    if request.method == "POST":
        form = TranscForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            transcation_amount = Decimal(clean_data.get('Transaction'))

            # Update the user's balance
            new_balance = user_balance.total_balance - transcation_amount
            user_balance.total_balance = new_balance
            user_balance.save()

            # Save the transaction with the cash-in type
            
            #we commit to false because we want to add all field first in the form we only provide 2 fields
            #the transaction type not yet
            transaction = form.save(commit=False)
            transaction.user_id = user_pk  # Set the user_id field
            transaction.transacation_type = "cashout"
            transaction.save()

            messages.success(request, "You have successfully cashed out.")
            return redirect('profile')
        else:
            messages.error(request, "There is an error in your form.")
            return redirect('cashout')
    else:
        form = TranscForm()

    return render(request, "cash_out.html", {'form': form})


def history(request):
    
    user_pk = request.session.get('user_id')
    
    # to grab multiple object have to use filter rather than get()
    user_history=Transaction.objects.filter(user_id=user_pk)
    context={"history":user_history}
    
    
    return render(request,"history.html",context=context)
        
   

    
    



