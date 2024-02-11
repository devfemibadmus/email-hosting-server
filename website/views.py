from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import View
from server.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('server')  # Redirect if user is already logged in
        return render(request, 'website/account/signin.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('server')
        else:
            return render(request, 'website/account/signin.html', {'error_message': 'Invalid username or password'})

class SignupPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('server')  # Redirect if user is already logged in
        return render(request, 'website/account/signup.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = CustomUser.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('server')
        else:
            return render(request, 'website/account/signup.html', {'error_message': 'Please provide both username and password'})

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

def signout(request):
    logout(request)
    return redirect('server')