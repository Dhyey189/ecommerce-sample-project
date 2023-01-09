from django.db import models
from django.db.models.signals import pre_save,post_save,pre_delete,post_delete
from django.dispatch import receiver
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
    image = models.ImageField(upload_to='images/')


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

class OrderDetails(models.Model): 
    order_details_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    product_price = models.IntegerField(default = 0)
    product_quantity = models.IntegerField()
    subtotal = models.IntegerField(default = 0)


'''
In a nutshell, signals allow certain senders to notify a set of receivers that some action has taken place.
They're especially useful when many pieces of code may be interested in the same events. 
Django's built-in signals let user code get notified of certain actions.

Signals: pre_save, post_save, pre_delete, post_delete, m2m_changed.

'''
# taking an example
@receiver(pre_save, sender = Customer)
def notify_customer_verify_email(sender,instance,*args,**kwargs):
    print(f"send a email verification link on {instance.email}")

@receiver(post_save, sender = Customer)
def notify_customer_account_created(sender,instance,created,*args,**kwargs):
    print(instance.customer_id)
    print(f"send a welcome email to the customer on {instance.email}")

@receiver(pre_delete, sender = Customer)
def tranfer_to_deleted_account_table(sender,instance,*args,**kwargs):
    print(f"Transfer the details of customer with id = {instance.customer_id} to deleted accounts table")

@receiver(post_delete, sender = Customer)
def notify_customer_account_deleted(sender,instance,*args,**kwargs):
    print(f"send a goodbye email to the customer on {instance.email}")

@receiver(pre_save, sender = OrderDetails)
def set_sub_total(sender,instance,*args,**kwargs):
    instance.product_price = instance.product_id.product_price
    instance.subtotal = instance.product_quantity * instance.product_price
# post_save.connect(notify_customer_account_created,sender = Customer)