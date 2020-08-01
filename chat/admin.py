from django.contrib import admin
from .models import UserProfile, Messages

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Messages)
