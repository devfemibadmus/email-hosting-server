from django.contrib.auth.decorators import login_required
from .decorator.authenticator import resolve_domain_record
from .models import EmailMessage, CustomUser, Domain
from django.contrib import messages
from django.shortcuts import render
from django.views import View
from .models import Domain

@login_required
def server(request):
    return render(request, 'server/email.html')

class DomainView(View):
    @login_required
    @resolve_domain_record
    def get(self, request, *args, **kwargs):
        domain = kwargs.get('domain') or request.GET.get('domain')
        if domain:
            if Domain.objects.filter(name=domain, user=request.user).exists():
                messages.success(request, f"{domain} associated with this account")
                domain_obj = Domain.objects.get(name=domain, user=request.user)
            else:
                messages.info(request, f"{domain} not associated with this account")
                domain_obj = None
        else:
            return redirect('server')
        return render(request, "server/domain.html", {'domain': domain_obj})

    @login_required
    @resolve_domain_record
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
                messages.warning(request, f"{domain} pointing to {mx_record}")
        else:
            messages.warning(request, "Domain parameter is missing")
            domain_obj = None
        return render(request, "server/domain.html", {'domain': domain_obj})
