from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Balance

# we want to automatically create an object after the user sign up
#we must be specified the initial value of the value of our balace to 0 because the user cant fill it during sign up 

@receiver(post_save, sender=User)
def create_user_balace(sender,instance,created,**kwargs):
    if created:
        Balance.objects.create(user=instance,total_balance=0)
    