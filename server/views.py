from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import EmailMessage, CustomUser, Subscription, CustomUser

@login_required
def server(request):
    return render(request, 'server/email.html')