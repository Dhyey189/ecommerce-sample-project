from django.urls import path,include
from rest_framework import routers
from . import views
from . import viewsets

router = routers.DefaultRouter()
router.register('customer_api_viewset',viewsets.CustomerViewSet)


urlpatterns = [
    path('customer_api/',views.customer_api),
    path('product_api/',views.product_api),
    path('api_auth/',include('rest_framework.urls')),
    path('product_api_generics/',viewsets.ProductListCreateAPIView.as_view()),
    path('product_api_generics/<int:pk>',viewsets.ProductRetriveAPIView.as_view()),
    path('product_api_generics/update/<int:pk>',viewsets.ProductUpdateAPIView.as_view()),
    path('product_api_generics/delete/<int:pk>',viewsets.ProductDeleteAPIView.as_view())
]
print(router.urls)
urlpatterns += router.urls