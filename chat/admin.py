from django.contrib import admin
from .models import UserProfile, Messages, Friends

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Messages)
admin.site.register(Friends)
