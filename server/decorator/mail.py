from functools import wraps
from django.contrib import messages
from ..models import Domain, EmailMessage


def validate_mailinfo(mailinfo):
    required_fields = ['body', 'subject', 'sendto']
    for field in required_fields:
        if field not in mailinfo or mailinfo[field] == "default":
            return False
    return True


def delete_mail(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        action = request.GET.get("action")
        mail_pk = request.GET.get("mail_pk")
        domain = request.GET.get("domain")
        if action == 'delete_mail' and Domain.objects.filter(name=domain).exists():
            if Domain.objects.filter(name=domain, user=request.user).exists() and EmailMessage.objects.filter(pk=mail_pk).exists():
                messages.success(request, 'Mail deleted successfully')
            else:
                messages.error(request, f'You dont have access to {domain}')
        return view_func(request, *args, **kwargs)
    return wrapper


def create_mail(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            domain_name = request.POST.get("domain")
            category = request.POST.get("category") or "inbox"
            body = request.POST.get("body") or "default"
            subject = request.POST.get("subject") or "default"
            sendto = request.POST.get("sendto") or "default"
            
            if Domain.objects.filter(name=domain_name).exists():
                domain_instance = Domain.objects.get(name=domain_name)
                if validate_mailinfo({'body': body, 'subject': subject, 'sendto': sendto}):
                    email_message = EmailMessage.objects.create(
                        domain=domain_instance, 
                        body=body, 
                        subject=subject, 
                        sender=sendto, 
                        category=category
                    )
                    messages.success(request, 'Mail created successfully')
                    return view_func(request, email_message=email_message, *args, **kwargs)
                else:
                    messages.error(request, 'Invalid mail info. Body, subject, and sender are required')
            else:
                messages.error(request, f'Domain "{domain_name}" does not exist')

            return view_func(request, *args, **kwargs)

        return view_func(request, *args, **kwargs)
    return wrapper

def get_mail(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        action = request.GET.get("action")
        mail_pk = request.GET.get("mail_pk")
        domain = request.GET.get("domain")
        
        if action == 'get_mail' and Domain.objects.filter(name=domain).exists():
            if Domain.objects.filter(name=domain, user=request.user).exists():
                if EmailMessage.objects.filter(pk=mail_pk, domain__name=domain).exists():
                    email_messages = EmailMessage.objects.get(pk=mail_pk, domain__name=domain)
                else:
                    email_messages = EmailMessage.objects.get(domain__name=domain)
                return view_func(request, email_messages=email_messages, *args, **kwargs)
            else:
                messages.error(request, f'You dont have access to {domain} or the requested mail does not exist')
        return view_func(request, *args, **kwargs)
    
    return wrapper
