from django.contrib import admin

# Register your models here.
from .models import CustomUser, VirtualDomains

admin.site.register(CustomUser)
admin.site.register(VirtualDomains)