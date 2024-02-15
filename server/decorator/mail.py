import re
from functools import wraps
from django.contrib import messages
from ..models import Domain, EmailMessage



def validate_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def validate_mail_account(sender):
    return True

def extract_domain(email):
    parts = email.split('@')
    if len(parts) != 2:
        return email
    return parts[1]

def extract_action_and_params(request):
    action = request.GET.get("action") or request.POST.get("action")
    mail_pk = request.GET.get("mail_pk") or request.POST.get("mail_pk")
    sender = request.GET.get("sender") or request.POST.get("sender")
    return action, mail_pk, sender

def validate_mail_info(mail_info):
    required_fields = ['body', 'subject', 'sendto']
    return all(mail_info.get(field) and mail_info.get(field) != "default" for field in required_fields)


def create_mail(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            mail_info = {
                'category': request.POST.get("category", "inbox"),
                'body': request.POST.get("body", "default"),
                'subject': request.POST.get("subject", "default"),
                'sender': request.POST.get("sender", "default"),
                'sendto': request.POST.get("sendto", "default")
            }
            domain_name = extract_domain(mail_info['sender'])
            if Domain.objects.filter(name=domain_name).exists():
                domain_instance = Domain.objects.get(name=domain_name)
                if (validate_mail_info(mail_info) and 
                        validate_mail_account(mail_info['sender']) and 
                        validate_email(mail_info['sendto'])):
                    email_message = EmailMessage.objects.create(domain=domain_instance, **mail_info)
                    messages.success(request, 'Mail created successfully')
                    return view_func(request, email_message=email_message, *args, **kwargs)
                else:
                    messages.error(request, 'Invalid mail information. Body, subject, sender, and valid recipient email are required')
            else:
                messages.error(request, f'Domain "{domain_name}" does not exist')

            return view_func(request, *args, **kwargs)

        return view_func(request, *args, **kwargs)
    return wrapper


def get_mail(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        action, mail_pk, sender = extract_action_and_params(request)
        if action == 'get_mail':
            domain_name = extract_domain(sender)
            if Domain.objects.filter(name=domain_name, user=request.user).exists():
                if mail_pk and EmailMessage.objects.filter(pk=mail_pk, domain__name=domain_name, sender=sender).exists():
                    email_message = EmailMessage.objects.get(pk=mail_pk, domain__name=domain_name)
                    return view_func(request, email_message=email_message, *args, **kwargs)
                else:
                    messages.error(request, 'You don\'t have access to this mail or the requested mail does not exist')
            else:
                messages.error(request, f'You don\'t have access to {domain_name} or the requested mail does not exist')

        return view_func(request, *args, **kwargs)
    
    return wrapper

def delete_mail(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        action, mail_pk, sender = extract_action_and_params(request)
        if action == 'delete_mail':
            domain_name = extract_domain(sender)
            if Domain.objects.filter(name=domain_name, user=request.user).exists() and mail_pk:
                if EmailMessage.objects.filter(pk=mail_pk, sender=sender).exists():
                    EmailMessage.objects.filter(pk=mail_pk, sender=sender).delete()
                    messages.success(request, 'Mail deleted successfully')
                else:
                    messages.error(request, 'You don\'t have access to this mail or the requested mail does not exist')
            else:
                messages.error(request, f'You don\'t have access to {domain_name}')

        return view_func(request, *args, **kwargs)
    return wrapper


