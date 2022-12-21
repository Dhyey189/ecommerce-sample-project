# we can create viewset itself in views.py but for understanding purposes I have created in different file.

from rest_framework import viewsets,generics
from rest_framework.response import Response
from .models import Customer,Product
from .serializers import CustomerSerializer,ProductSerializer,ProductImageSerializer
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import NotFound,NotAcceptable,APIException
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,DjangoModelPermissions
from rest_framework.authentication import SessionAuthentication,TokenAuthentication,BasicAuthentication

from rest_apis.permissions import CustomDjangoModelPermissions
from rest_apis.authentications import CustomTokenAuthentication

# Implemented authentication classes and permission classes and validators(used in CustomerSerializers)
# they can be specific to particular view or can be genralized to whole api in settings.py 
class CustomerViewSet(viewsets.ModelViewSet):
    '''
    Methods provided by ModelViewSet

    list => base/customer_api_viewset (get)
    retrieve => base/customer_api_viewset/id (get)
    create => base/customer_api_viewset (post)
    update => base/customer_api_viewset/id (put)
    destroy => base/customer_api_viewset/id (delete)

    Classes which ModelViewSet inherits:- (mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet)
    
    '''
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'pk' #default

    # Format = 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
    # authentication_classes = [TokenAuthentication]

    # Format = 'Authorization: Bearer 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
    authentication_classes = [CustomTokenAuthentication]

    # authentication_classes = [SessionAuthentication]
    # authentication_classes = [BasicAuthentication]

    '''
    used permission classes to check whether the entity requesting resourse is authorized or not.
    different permission classes = [AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly,DjangoModelPermissions]

    DjangoModelPerssions is the permission which all the users has over all models(basically the super user has given to all the users)
    By default It allow get methods to all users but we can chage by creating custom permissions.
    '''
    # permission_classes = [DjangoModelPermissions]
    permission_classes = [CustomDjangoModelPermissions]
    
    '''
    calling create method which uses create method of super class mixins.CreateModelMixin,
    we can also skip this if we do not want any specific task to be done.
    similarly for all other request like list, update, destroy etc.
    '''
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    '''
    Overriding update method of super class mixins.UpdateModelMixin 
    but it can also be skipped, if we do not want any specific task to be done.
    '''
    def update(self,request,*args,**kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



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


