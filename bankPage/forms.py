from django import forms
from .models import *
from django.contrib.auth.models import User


class Userform(forms.ModelForm):
    
    class Meta:
        
        # state which table or model we need
        model = User
        
        #the name of the header title in our models, for this we using the auth_user models
        #the name in the form in html also must same as below
        fields =["first_name","last_name","email","username","password"]