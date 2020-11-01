from django.urls import path
from log_pay.views import *
from . import views
app_name = 'log_pay'
urlpatterns = [
    path('accounts/registration/', views.registration, name='registration'),
    path('index/', views.index, name='index'),
    path('', views.mission, name='mission'),
    path('types/<int:types_id>/', views.types, name='types'),
    path('eyJ1Ijoic2FkcmlrIiwiYSI6ImNrZ3ZhNWhrZDBpbXgycXJ5Z2cwNmFzZTcifQ.cxbz_15TzOfpWeFafy3sUQ/', views.one, name='one'),
]