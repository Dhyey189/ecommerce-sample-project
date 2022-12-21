from rest_framework import serializers
from .models import Customer,Product,Order,OrderDetails,ProductImage

from rest_apis.validators import validate_email,unique_email

# Using simple Serializer
class CustomerSerializer(serializers.Serializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(),required=False)
    name = serializers.CharField(max_length=50)
    # used validators for checking if email is in valid email format and unique.
    email = serializers.CharField(max_length=100,validators=[validate_email,unique_email])
    password = serializers.CharField(max_length=50,default = 'Aa@1Bb*2',required=False)
    address = serializers.CharField(max_length=500)
    mobile = serializers.CharField(max_length=15)

    def create(self,validated_data):
        # ** is for kwargs (key worded arguments) key, value.
        return Customer.objects.create(**validated_data)

    def update(self,instance,validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.email = validated_data.get('email',instance.email)
        instance.password = validated_data.get('password',instance.password)
        instance.address = validated_data.get('address',instance.address)
        instance.mobile = validated_data.get('mobile',instance.mobile)
        instance.save()
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