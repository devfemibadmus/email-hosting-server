from . import views
from django.urls import path

urlpatterns = [
    path('domain/', Domain.as_view(), name='domain'),
    path('domain/<str:domain>/', Domain.as_view(), name='domain_with_param'),
]
