from django.contrib import admin
from .models import *

# Register your models here.

#to be able to see the data in admin area in the website
admin.site.register(Balance)
admin.site.register(Transaction)