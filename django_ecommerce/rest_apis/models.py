from django.db import models

# Create your models here.

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50,default = 'Aa@1Bb*2')
    address = models.CharField(max_length=500)
    mobile = models.CharField(max_length=15)

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_desc = models.CharField(max_length=1000)
    product_price = models.IntegerField()

class ProductImage(models.Model):
    product_image_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.CharField(max_length=2000)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

class OrderDetails(models.Model): 
    order_details_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    product_price = models.IntegerField()
    product_quantity = models.IntegerField()
    subtotal = models.IntegerField()