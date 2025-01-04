from django.urls import path
from . import views

urlpatterns = [
    path('', views.coordinator, name='coordinator'),
    path('generate_qr/', views.generate_and_save_qr, name='generate_qr'),
]
