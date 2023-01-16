from django.contrib import admin

# Register your models here.
from .models import UserToken

admin.site.register(UserToken)
