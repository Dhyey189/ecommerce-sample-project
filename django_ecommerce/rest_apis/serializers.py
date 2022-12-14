from rest_framework import serializers
from .models import Customer,Product,Order,OrderDetails,ProductImage

# Using simple Serializer
class CustomerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=500)
    mobile = serializers.CharField(max_length=15)

    def create(self,validated_data):
        # ** is for kwargs (key worded arguments) key, value.
        print(validated_data)
        return Customer.objects.create(**validated_data)

    def update(self,instance,validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.email = validated_data.get('email',instance.email)
        instance.address = validated_data.get('address',instance.address)
        instance.moblie = validated_data.get('moblie',instance.moblie)
        return instance
    

# Using inbuilt ModelSerializer
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['product_id','product_name','product_desc','product_price']
        # exclude = ['image1','image2','image3']

# Using inbuilt ModelSerializer
class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'