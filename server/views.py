from django.contrib.auth.decorators import login_required
from .decorator.authenticator import resolve_domain_record
from .models import EmailMessage, CustomUser, Domain
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import render, redirect
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
        if domain:
            mx_record = request.mx_record
            txt_record = request.txt_record
            if mx_record:
                if Domain.objects.filter(name=domain, user=request.user).exists():
                    if Domain.objects.filter(name=domain, user=request.user, txt_record=request.user.txt_record).exists():
                        messages.info(request, f"{domain} already associated with your account")
                    else:
                        messages.warning(request, f"{domain} TXT record is incorrect")
                else:
                    if txt_record:
                        messages.success(request, f"{domain} TXT record verified")
                        domain_obj = Domain.objects.create(name=domain, user=request.user, txt_record=request.user.txt_record)
                    else:
                        messages.warning(request, f"{domain} TXT record is incorrect")
            else:
                messages.warning(request, f"MX record {domain} pointing to {mx_record}")
        else:
            messages.warning(request, "Domain parameter is missing")
        return render(request, "server/domain.html", {'domain': domain_obj})