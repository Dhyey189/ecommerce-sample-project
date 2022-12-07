from django.shortcuts import render
from .models import Customer,Order,OrderDetails,Product,ProductImage
# Create your views here.

def home(request):
    customer = list(Customer.objects.all())
    order = list(Order.objects.all())
    orderdetails = list(OrderDetails.objects.all())
    product = list(Product.objects.all())
    productimage = list(ProductImage.objects.all())
    # print(customer)
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
        # c.save()
    customer = list(Customer.objects.all())
    return render(request, 'customer.html', {"Customer": customer,'process' : 'donothing'})



