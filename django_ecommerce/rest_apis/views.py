from django.shortcuts import render
from .models import Customer,Product,Order,OrderDetails,ProductImage
from rest_framework.parsers import JSONParser
from .serializers import CustomerSerializer,ProductSerializer,ProductImageSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from rest_framework.exceptions import NotFound
# Create your views here.

# Different ways to return data in views
# HttpResponse for repsonse in http
# JsonResponse for response in json
# Response for response in any format
# Render for rendering templates with context dictionary in simple django framework
# JSONParser for parsing JSON data


# For parsing data 
# https://www.django-rest-framework.org/api-guide/parsers/#api-reference





@csrf_exempt
# used simple Serializer
def customer_api(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        customer = CustomerSerializer(data = data)
        if customer.is_valid():
            # not needed to call save method here bcz we have called create method in serializers itlself.
            # customer.save()
            return JsonResponse(customer.data, status = 201)
        return JsonResponse(customer.error, status = 400)
    elif request.method == 'GET':
        customer = Customer.objects.all()
        c = CustomerSerializer(customer,many=True) 
        return JsonResponse(c.data,safe = False,status = 200)

@api_view(['POST','GET'])
@transaction.atomic
@csrf_exempt
def product_api(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        product = ProductSerializer(data = {'product_name' : data['product_name'] ,'product_desc' : data['product_desc'], 'product_price' : data['product_price']})
        if product.is_valid():
            product.save()
            # saving product data
            print(product.data)
            # Fetching product_id 
            product_id = product.data['product_id']
            # Now Saving each image in ProductImage model using product_id
            images = [data['image1'],data['image2'],data['image3']]   
            for i in images:
                productimage = ProductImageSerializer(data = {'product_id':product_id,'image':i})
                if productimage.is_valid():
                    productimage.save()
                else :
                    return Response(productimage.error,status = 400)
            return Response(product.data,status = 201)
        return Response(product.error,status = 400)
    elif request.method == 'GET':
        # fetching product details using product_id
        if request.query_params.get('product_id'):
            id = request.query_params['product_id']
            # exception handling if product id does not exist.
            # For excep
            try:
                product = Product.objects.get(product_id = id)
                p = ProductSerializer(product)
            except Product.DoesNotExist:
                raise NotFound(detail = 'product with product_id = ' + id + ' does not exist!', code = 404)
            else:
                return Response(p.data,status = 200)
        # fetching all products.
        else:
            products = Product.objects.all()
            p = ProductSerializer(products,many = True)
            return Response(p.data,status = 200)




# {
# 	"product_name" : "Laptop",
# 	"product_desc" : "Dell, i5, 8gb ram",
# 	"product_price" : "70000",
# 	"image1" : "https://abc.com",
# 	"image2" : "https://xyz.com",
# 	"image3" : "https://pqr.com"
# }