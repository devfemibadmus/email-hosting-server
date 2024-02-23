from functools import wraps
from django.conf import settings
from django.contrib import messages
from ..operator.dns_checker import DNSChecker
from ..models import VirtualDomain

def resolve_domain_record(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        domain_name = kwargs.get('domain') or request.GET.get('domain') or request.POST.get('domain')
        if domain_name:
            checker = DNSChecker()
            mx_record = checker.verify_mx(domain_name, settings.MX_RECORD)
            txt_record = checker.verify_txt(domain_name, request.user.txt_record)
            
            if mx_record is True:
                messages.success(request, "MX record found")
            elif mx_record is False:
                messages.error(request, "MX record not found")
            else:
                messages.error(request, mx_record)
            
            if txt_record is True:
                messages.success(request, "TXT record found")
                domain_obj, created = VirtualDomain.objects.get_or_create(name=domain_name, user=request.user, txt_record=request.user.txt_record)
                request.domain_obj = domain_obj
            elif txt_record is False:
                messages.error(request, "TXT record not found")
                messages.info(request, f'Add txt record {request.user.txt_record}')
            else:
                messages.error(request, txt_record)
        else:
            messages.error(request, "Domain parameter is missing")

        return view_func(request, *args, **kwargs)
    
    return wrapper
