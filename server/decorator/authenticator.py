from functools import wraps
from django.contrib import messages
from ..operator.dns_resolver import DomainResolver

def resolve_domain_record(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        domain = kwargs.get('domain') or request.GET.get('domain') or request.POST.get('domain')
        if domain:
            resolver = DomainResolver()
            resolver.QUERY_TYPE = resolver.QUERY_TYPE_MX
            mx_record = resolver.resolve_domain(domain)
            resolver.QUERY_TYPE = resolver.QUERY_TYPE_TXT
            txt_record = resolver.resolve_domain(domain)
            if mx_record:
                request.mx_record = mx_record
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
