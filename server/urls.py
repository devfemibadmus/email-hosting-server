from . import views
from django.urls import path

urlpatterns = [
    path('', views.server, name='server'),
    path('message/', views.MessagesView.as_view(), name='domain'),
    path('domain/', views.DomainView.as_view(), name='domain'),
    path('domain/<str:domain>/', views.DomainView.as_view(), name='domain'),
]
