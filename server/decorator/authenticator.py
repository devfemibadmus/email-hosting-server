from functools import wraps
from django.conf import settings
from django.contrib import messages
from ..operator.dns_checker import DNSChecker
from ..models import Domain

def resolve_domain_record(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        domain = kwargs.get('domain') or request.GET.get('domain') or request.POST.get('domain')
        if domain:
            checker = DNSChecker()
            request.mx_record = checker.verify_mx(domain, settings.MX_RECORD)
            request.txt_record = checker.verify_txt(domain, request.user.txt_record)
            if request.mx_record == True:
                messages.error(request, "MX record found")
            elif request.mx_record == False:
                messages.error(request, "MX record not found")
            else:
                messages.error(request, request.mx_record)
            if request.txt_record == True:
                messages.success(request, "my TXT record found")
                domain_obj, available = Domain.objects.get_or_create(user=request.user, name=domain, txt_record=request.user.txt_record)
                request.domain_obj = domain_obj
            elif request.txt_record == False:
                messages.success(request, "my TXT record not found")
            else:
                messages.error(request, request.txt_record)
        else:
            messages.error(request, "Domain parameter is missing")
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
