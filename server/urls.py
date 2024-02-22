from . import views
from django.urls import path

urlpatterns = [
    path('', views.server, name='server'),

    path('domain/', views.DomainView.as_view(), name='domain'),
    path('<str:domain>/', views.DomainView.as_view(), name='domain_name'),
    path('domain/<str:domain>/', views.DomainView.as_view(), name='domain__domain_name'),
    

    path('domain/mails/', views.MessagesView.as_view(), name='mails'),
    path('<str:domain>/mails/', views.MessagesView.as_view(), name='domains_name__mails'),
    path('domain/<str:domain>/mails/', views.MessagesView.as_view(), name='domain__domain_name__mails'),
]
