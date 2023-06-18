from django.db import models

# import pre-built models for crearting user 
from django.contrib.auth.models import User



# Create your models here.
# setup a database

#######################################################################
#class SignUp(models.Model):
    
    # create a table in database 
#    name = models.CharField(max_length=50)
#    email = models.EmailField(max_length=100)
#    password = models.CharField(max_length=50)
#    balance= models.DecimalField(max_digits=14, decimal_places=2)
#######################################################################


class Balance(models.Model):
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # to key in the user balance  
    total_balance = models.DecimalField(max_digits=24,decimal_places=2)
    
    
    
    
    def __str__(self):
        return self.user.username + " " + "("+ str(self.Balance) + ")"
    
class Transaction(models.Model):
    
    
    #this user will find the user based on the uniq key that the user has
     
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    
    #transaction data
    Transaction = models.DecimalField(max_digits=24,decimal_places=2)
    
    #transcripton
    Transcription=models.CharField(max_length=150)
    
    def __str__(self):
        return self.user.username + " (" + self.Transcription +")"
    
    
    
    
    
   
    