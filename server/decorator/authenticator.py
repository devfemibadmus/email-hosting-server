from functools import wraps
from django.contrib import messages
from ..operator.dns_checker import DNSChecker

def resolve_domain_record(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        domain = kwargs.get('domain') or request.GET.get('domain') or request.POST.get('domain')
        if domain:
            checker = DNSChecker()
            request.mx_record = checker.verify_mx(domain, "mail.blackstackhub.com.")
            request.txt_record = checker.verify_txt(domain, request.user.txt_record)
            if mx_record:
                if mx_record != "mail.blackstackhub.com":
                    messages.error(request, f"MX record pointing to {mx_record}")
                else:
                    messages.success(request, f"MX record pointing to {mx_record}")
            else:
                messages.error(request, f"MX record not found for the {domain}")
        else:
            messages.error(request, "Domain parameter is missing")
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
