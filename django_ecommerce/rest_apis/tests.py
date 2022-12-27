from django.test import TestCase,Client

# Create your tests here.
from model_bakery import baker
from .models import Customer,Product

# manually
class CustomerTestModel(TestCase):
    """
    Class to test the model Customer
    """

    def setUp(self):
        Customer.objects.create(name='DP1' , email='dp1@gmail.com', address='AMD', mobile = '123' )

    def test_customer_created(self):
        c = Customer.objects.get(email = 'dp1@gmail.com')
        self.assertEqual(c.email,'dp1@gmail.com')


# using model bakery
class ProductTestModel(TestCase):

    def setUp(self):
        self.products = baker.prepare(Product,_quantity = 3)
    
    def test_product_created(self):
        self.assertEqual(len(self.products),3)


class CustomerTestAPI(TestCase):

    def setUp(self):
        self.customers = baker.make(Customer,_quantity = 5)

    def test_customer_get_api(self):
        c = Client()
        response1 = c.get('/rest_api/customer_api_viewset/')
        response2 = c.get('/rest_api/customer_api_viewset/7/')
        # print(response1.json(),'\n\n\n',response2.json())
        self.assertEqual(response1.status_code,200)
        self.assertEqual(response2.status_code,200)

    def test_customer_post_api(self):
        c = Client()
        response = c.post('/rest_api/customer_api_viewset/',{"name" : "John",
            "email" : "john@gmail.com" ,
            "address" : "Ahmedabad",
            "mobile" : "0123498765"})
        count = Customer.objects.all().count()
        # 5 count was already there
        self.assertEqual(count,6)
        self.assertEqual(response.status_code,201)

    def test_customer_delete_api(self):
        c = Client()
        response1 = c.delete('/rest_api/customer_api_viewset/2/')
        response2 = c.get('/rest_api/customer_api_viewset/2/')
        self.assertEqual(response1.status_code,204)
        self.assertEqual(response2.status_code,404)

    def test_customer_update_api(self):
        c = Client()
        response1 = c.put('/rest_api/customer_api_viewset/18/',data = {"name": "Updated Name",
            "email": "updatedemail@gmail.com",
            "address": "Ahmedabad",
            "mobile": "8192838492"},content_type='application/json')
        
        response2 = c.get('/rest_api/customer_api_viewset/18/')
        new_name = response2.json()['name']
        print("new name is: ",new_name)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(new_name, "Updated Name")

        
        




    