from django.shortcuts import render
from .models import Customer,Order,OrderDetails,Product,ProductImage
from django.db import transaction
# Create your views here.

def welcome(request):
    return render(request,'welcome.html')

@transaction.atomic
def home(request):
    customer = list(Customer.objects.all())
    order = list(Order.objects.all())
    orderdetails = list(OrderDetails.objects.all())
    product = list(Product.objects.all())
    productimage = list(ProductImage.objects.all())
    # print(customer)
    if request.method == 'POST' and 'create_order' in request.POST:
        product_quantity = request.POST.get('product_quantity')
        p = Product.objects.get(product_id = int(request.POST.get('product_id')))
        print(int(request.POST.get('product_id')))
        c = Customer.objects.get(customer_id = int(request.POST.get('customer_id')))
        c.save()
        o = Order(customer_id = c)
        o.save()
        od  = OrderDetails(product_price = p.product_price,product_quantity = product_quantity, subtotal = int(p.product_price)*int(product_quantity) , order_id = o, product_id = p) 
        od.save()

    return render(request, 'home.html', {"Customer": customer, "Order": order, "OrderDetails": orderdetails,"Product": product, "ProductImage": productimage})

def manage_customer(request):
    
    if request.method == 'POST' and 'Create' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        # Insert method 1:- using create
        # Customer.objects.create(name = name,email = email, address = address, mobile = mobile)
        
        # Insert method 2:- directly entering data and then saving the data.
        c = Customer(name = name,email = email, address = address, mobile = mobile)
        c.save()
        customer = list(Customer.objects.all())
        return render(request, 'customer.html', {"Customer": customer, 'process' : 'post'})
    elif request.method == 'GET' and 'Find' in request.GET:
        c = list(Customer.objects.filter(customer_id = request.GET.get('id')))
        customer = list(Customer.objects.all())
        return render(request, 'customer.html', {"Customer": customer,'customer' : c,'process' : 'get'})
    elif request.method == 'POST' and 'Update' in request.POST :
        id = request.POST.get('id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        # update method 1:-  using get and then updating data manually and then saving in database  
        c = Customer.objects.get(customer_id = id)
        c.name = name
        c.email = email
        c.address = address
        c.mobile = mobile
        c.save()

        # update method 2:- using filter and then update function.
        # Customer.objects.filter(customer_id = id).update(name = name,email = email, address = address, mobile = mobile)

        # Below method should only be followed by if primary key is unique in it.
        # Customer.objects.update_or_create(customer_id = id,name = name,email = email, address = address, mobile = mobile)
        customer = list(Customer.objects.all())
        return render(request, 'customer.html', {"Customer": customer,'process' : 'put'})
    elif request.method == 'POST' and 'Delete' in request.POST :
        # Method 1
        Customer.objects.filter(customer_id = request.POST.get('id')).delete()

        # Method 2
        # c = Customer.objects.get(customer_id = request.POST.get('id'))
        # c.delete()
    customer = list(Customer.objects.all())
    return render(request, 'customer.html', {"Customer": customer,'process' : 'donothing'})

@transaction.atomic
def manage_product(request):
    # For adding new products in the list
    if request.method == 'POST' and 'Create' in request.POST:
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        price = request.POST.get('price')
        p = Product(product_name = name,product_desc = desc,product_price = price)
        p.save()
        images_count = int(request.POST.get('images_count'))
        for i in range(1,images_count+1):
            link = request.POST.get('image'+str(i))
            print('image'+str(i))
            img = ProductImage(product_id = p,image = link)
            img.save()

    # For deleting existing products
    # In this transaction if the product details is deleted then the tables order and order details need to be 
    # deleted in sort the order should be cancelled, should be deleted from exsisting order and order details tables
    # ideally the data should be moved to cancelled_orders table....
    # below is the series of transcation of deletion of product along with deleting order and order details entries.
    elif request.method == 'POST' and 'Delete' in request.POST:
        with transaction.atomic():
            id = request.POST.get('id')
            p = Product.objects.get(product_id = int(id))
            order_to_be_deleted = []
            order_details = OrderDetails.objects.filter(product_id = p.product_id)
            order_details = list(order_details)
            p.delete() 
            for od in order_details:
                order_to_be_deleted.append(od.order_id)
            OrderDetails.objects.filter(product_id = id).delete()
            for oid in order_to_be_deleted:
                Order.objects.filter(order_id = oid.order_id).delete()
            


    # For updating products
    elif request.method == 'POST' and 'Update' in request.POST:
        id = request.POST.get('id')
        p = Product.objects.get(product_id = id)
        p.product_name = request.POST.get('name')
        p.product_desc = request.POST.get('desc')
        p.product_price = request.POST.get('price')
        p.save()
    product = list(Product.objects.all())
    productimage = list(ProductImage.objects.all())
    return render(request, 'product.html',{"Product": product, "ProductImage": productimage})




