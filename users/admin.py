from django.contrib import admin

# Register your models here.
# thats important to remember: new models have to be added here \/

from .models import Profile
admin.site.register(Profile)