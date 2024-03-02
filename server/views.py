from .decorator.mail import get_mail, create_mail, delete_mail
from .decorator.authenticator import resolve_domain_record
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from .models import VirtualDomains

class DomainView(View):
    @method_decorator(login_required)
    @method_decorator(resolve_domain_record)
    def dispatch(self, request, *args, **kwargs):
        return render(request, "server/home.html")

class MessagesView(View):
    @method_decorator(login_required)
    @method_decorator(get_mail)
    @method_decorator(create_mail)
    @method_decorator(delete_mail)
    def dispatch(self, request, *args, **kwargs):
        email_message = kwargs.get('email_message')
        messages_list = {message.tags: message.message for message in messages.get_messages(request)}
        response_data = {
            'email_message': email_message,
            'messages': messages_list
        }
        return JsonResponse(response_data)



