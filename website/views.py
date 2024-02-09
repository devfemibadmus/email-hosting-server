from django.shortcuts import render

def home(request):
    return render(request, 'website/home.html')
    
def about(request):
    return render(request, 'website/about.html')

def contact(request):
    return render(request, 'website/contact.html')
    
def privacy(request):
    return render(request, 'website/privacy.html')
    
def security(request):
    return render(request, 'website/security.html')