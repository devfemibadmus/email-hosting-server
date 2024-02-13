from . import views
from django.urls import path

urlpatterns = [
    path('', views.server, name='server'),
    path('domain/<str:domain>/', views.DomainView.as_view(), name='domain_with_param'),
]
