from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from .forms import Userform,TranscForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
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
    
 
@login_required(login_url="home-page")
def profile(request):
    
    
    user_pk= request.session.get('user_id')
    
    user=User.objects.get(id=user_pk)
    username=user.username
    
    user_balance=Balance.objects.get(user_id=user_pk)    
        
    return render(request,'profile.html',context={"username":username,"Balance":user_balance.total_balance})


# THIS VIEW NOT DONE YET SENT RECEIVER ID AND AMOUNT TO SESSION 
# TO BE USED IN NEXT CONFIRMATION VIEW
def transfer(request):
    
    user_pk= request.session.get('user_id')
    sender=User.objects.get(id=user_pk)
    
    if request.method == "POST":
        
        
        receiver_id= request.POST.get('receipient')
        amount=request.POST.get('amount')
        
        
        
        # if the form is not null
        if receiver_id and amount:
            #if the receiver in the object it will render confirmation.html
            receiver = get_object_or_404(User, username=receiver_id)

            #save the receiver id to be used in confirmation view
            request.session['receiver_id'] = receiver.id 
            
            #save the amount to be used in confirmation view
            request.session['amount'] = amount
            #avoid using render if there something you want to pass in the if statement
            # it only will run the html without run the view 
            return redirect("confirmations")
        else:
            messages.error(request, "Please provide a valid receiver and amout was not null.")
            return render(request, "transfer.html")

    
    return render(request,"transfer.html")

def confirmation(request):
    
    transaction_amount=Decimal(request.session.get("amount"))
    ### find sender name##
    user_pk= request.session.get('user_id')
    sender=User.objects.get(id=user_pk)
    

    
    ### find receiver name to update into the transcription ##
    receiver_id=request.session.get('receiver_id')   
    receiver=User.objects.get(id=receiver_id)
    
    
    
    
    
    if request.method == "POST":
        
        #get the receiver object and update the total balance
        receiver_balance= Balance.objects.get(user_id=receiver_id)
        receiver_balance.total_balance = receiver_balance.total_balance + transaction_amount
        receiver_balance.save()
        
        
        receiver_transaction = transaction_amount
        receiver_transcription="Receive cash from " + sender.username
        receiver_transfer_type="cashin"
        
        
        #create the receiver transaction object
        receiver_instance_create=Transaction(Transaction=receiver_transaction,
                                             Transcription=receiver_transcription,
                                             transacation_type=receiver_transfer_type,
                                             user_id=receiver_id)
        
        receiver_instance_create.save()
        
    
        #get the sender object and update the total balance
        sender_balance = Balance.objects.get(user_id=user_pk)
        sender_balance.total_balance = sender_balance.total_balance - transaction_amount
        sender_balance.save()
        
        #create the sender transaction object
        sender_transaction = transaction_amount
        sender_transcription="transfer cash to " + receiver.username
        sender_transfer_type="cashout"
        
        sender_instance_create=Transaction(Transaction=sender_transaction,
                                             Transcription=sender_transcription,
                                             transacation_type=sender_transfer_type,
                                             user_id=user_pk)
        
        sender_instance_create.save()
        
    

        
        messages.success(request, "You have successfully transfer.") 
        return redirect("profile")
    
    
    
    
    
    return render(request, "confirmation.html",{"receiver":receiver,"amount":transaction_amount})


    


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


def navbar(request):
    
    return render(request,"navbar.html")

def logoutuser(request):
    
    logout(request)
    return redirect("home-page")
    
        
   

    
    

