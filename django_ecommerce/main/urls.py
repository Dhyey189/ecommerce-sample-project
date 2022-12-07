from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name = 'home'),
    path('customer/', views.manage_customer,name = 'customer')
]