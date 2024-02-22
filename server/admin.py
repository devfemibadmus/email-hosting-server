from django.contrib import admin

# Register your models here.
from .models import CustomUser, VirtualDomain

admin.site.register(CustomUser)
admin.site.register(VirtualDomain)