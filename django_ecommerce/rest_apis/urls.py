from django.urls import path,include
from rest_framework import routers
from . import views


# router = routers.DefaultRouter()
# router.register(r'customer_api/',views.customer_api)

urlpatterns = [
    # path('',include(router.urls)),
    path('customer_api/',views.customer_api),
    path('product_api/',views.product_api),
    # path('api-auth/',include('rest_framework.urls'))
]