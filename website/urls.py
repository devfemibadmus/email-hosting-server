from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('privacy/', views.privacy, name="privacy"),
    path('security/', views.security, name="security"),
    
    path('signin/', views.LoginPage.as_view(), name='login'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.SignupPage.as_view(), name='signup'),
]
