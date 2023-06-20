from django import forms
from .models import *
from django.contrib.auth.models import User


class Userform(forms.ModelForm):
    
    
    #must be state to encrypt the password
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        
        # state which table or model we need
        model = User
        
        #the name of the header title in our models, for this we using the auth_user models
        #the name in the form in html also must same as below
        fields =["first_name","last_name","email","username","password"]
        
    #to encrypt the password form  
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            # Encrypt the password
            user.set_password(password)
        if commit:
            user.save()
        return user

class TranscForm(forms.ModelForm):
    
    class Meta:
        
        model=Transaction
        fields=["Transaction","Transcription"]
    
