from . import views
from django.urls import path

urlpatterns = [
    path('', views.DomainView.as_view(), name='server'),
    path('<str:domain>/', views.DomainView.as_view(), name='domain'),
    path('mail/<str:domain>/', views.MessagesView.as_view(), name='domain_mails'),
]
