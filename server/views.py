from .decorator.mail import get_mail, create_mail, delete_mail
from .decorator.authenticator import resolve_domain_record
from django.contrib.auth.decorators import login_required
from .models import EmailMessage, CustomUser, Domain
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from .models import Domain


@login_required
def server(request):
    return render(request, 'server/email.html')

class DomainView(View):
    @method_decorator(login_required)
    @method_decorator(resolve_domain_record)
    def get(self, request, *args, **kwargs):
        domain = kwargs.get('domain') or request.GET.get('domain')
        if not domain:
            return redirect('server')
        return render(request, "server/domain.html", {'domain': domain})

    @method_decorator(login_required)
    @method_decorator(resolve_domain_record)
    def post(self, request, *args, **kwargs):
        domain = request.POST.get('domain')
        if not domain:
            messages.warning(request, "Domain parameter is missing")
            return render(request, "server/domain.html")

        mx_record = request.mx_record
        txt_record = request.txt_record

        if not mx_record:
            messages.warning(request, f"MX record for {domain} is missing")
        elif not txt_record:
            messages.warning(request, f"TXT record for {domain} is incorrect")
        else:
            if Domain.objects.filter(name=domain, user=request.user, txt_record=request.user.txt_record).exists():
                messages.info(request, f"{domain} is already associated with your account")
            else:
                messages.success(request, f"{domain} TXT record verified")
                Domain.objects.create(name=domain, user=request.user, txt_record=request.user.txt_record)

        return render(request, "server/domain.html", {'domain': domain})

class MessagesView(View):
    @method_decorator(login_required)
    @method_decorator(get_mail)
    @method_decorator(create_mail)
    @method_decorator(delete_mail)
    def dispatch(self, request, *args, **kwargs):
        email_message = kwargs.get('email_message')
        email_message_dict = {
            'sender': email_message.sender,
            'sendto': email_message.sendto,
            'domain': email_message.domain.name,
            'subject': email_message.subject,
            'body': email_message.body,
            'sent_at': email_message.sent_at.isoformat() if email_message.sent_at else None,
            'is_read': email_message.is_read,
            'is_starred': email_message.is_starred,
            'security_info': None
        }
        messages_list = {message.tags: message.message for message in messages.get_messages(request)}
        response_data = {
            'email_message': email_message_dict,
            'messages': messages_list
        }
        if not request.GET.get("integrate"):
            return JsonResponse(response_data)
        return render(request, 'server/email.html', {'email_message': email_message, 'messages': messages_list})

