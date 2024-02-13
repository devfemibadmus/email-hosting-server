from django.contrib import admin

# Register your models here.
from .models import CustomUser, Domain

admin.site.register(CustomUser)
admin.site.register(Domain)