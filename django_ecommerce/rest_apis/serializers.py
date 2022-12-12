from rest_framework import serializers
from .models import Customer,Product,Order,OrderDetails,ProductImage


class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ('customer_id','name','email','address','mobile')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['product_id','product_name','product_desc','product_price']
        # exclude = ['image1','image2','image3']

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'