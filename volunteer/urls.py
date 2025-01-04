from django.urls import path
from . import views

urlpatterns = [
    path('', views.volunteer, name='volunteer'),
    path('allotactivity/', views.allot_activity, name='allotactivity'),
]
