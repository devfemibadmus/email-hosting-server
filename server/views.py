from django.shortcuts import render
from django.http import JsonResponse
from helper import DomainResolver as MXRecord
from django.contrib.auth.decorators import login_required
from .models import EmailMessage, CustomUser, Subscription, CustomUser

@login_required
def server(request):
    return render(request, 'server/email.html')

@login_required
def addDomain(request, domain):
    valid = False
    mx = MXRecord.resolve_domain(domain)
    if mx == "mail.blackstackhub.com":
        valid = True
    return render(request, 'server/email.html', {'valid': valid})

from django.shortcuts import render
from decorator.authenticator import resolve_mx_record

@login_required
@resolve_mx_record
def my_view(request, domain=None, mx_record=None):
    if mx_record:
        context = {
            'mx_record': mx_record,
        }
        return render(request, 'template.html', context)
    else:
        return render(request, 'error.html', {'error_message': 'MX record not found'})
        
class Domain(View):
    @resolve_mx_record
    @login_required
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            domain = kwargs.get('domain') or request.GET.get('domain')
        elif request.method == 'POST':
            domain = request.POST.get('domain')
        else:
            domain = None

        if domain:
            if domain not in request.user.domain:
                messages.warning(request, f"{domain} not associated with your account")
        else:
            domain = request.user.domain

        return render(request, "server/domain.html", {'domain': domain})
