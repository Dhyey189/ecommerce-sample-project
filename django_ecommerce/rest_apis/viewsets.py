# we can create viewset itself in views.py but for understanding purposes I have created in different file.

from rest_framework import viewsets,generics
from rest_framework.response import Response
from .models import Customer,Product
from .serializers import CustomerSerializer,ProductSerializer,ProductImageSerializer
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import NotFound,NotAcceptable,APIException

class CustomerViewSet(viewsets.ModelViewSet):
    '''
    Methods provided by ModelViewSet

    list => base/customer_api_viewset
    retrieve => base/customer_api_viewset/id
    
    '''
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'pk' #default


class ProductListCreateAPIView(generics.ListCreateAPIView):
    '''
    list => base/product_api_generics (get)
    create => base/product_api_generics (post)
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' #default

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        try:
            instance = ProductSerializer(data = {'product_name' : data['product_name'] ,'product_desc' : data['product_desc'], 'product_price' : data['product_price']})
        except:
            raise APIException(detail = 'server error or fields missing or incorrect!') 
        else:
            if instance.is_valid() :
                instance.save()
                product_id = instance.data['product_id']
                # Now Saving each image in ProductImage model using product_id
                images = [data['image1'],data['image2'],data['image3']]   
                for i in images:
                    productimage = ProductImageSerializer(data = {'product_id':product_id,'image':i})
                    if productimage.is_valid():
                        productimage.save()
                    else :
                        raise NotAcceptable(detail = productimage.error)
                return Response(instance.data)
            raise NotAcceptable()

class ProductRetriveAPIView(generics.RetrieveAPIView):
    '''
    retrieve => base/product_api_generics/id
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdateAPIView(generics.UpdateAPIView):
    '''
    update => base/product_api_genrics/update/id
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDeleteAPIView(generics.DestroyAPIView):
    '''
    destroy => base/product_api_genrics/delete/id
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


