from django.test import TestCase,Client
from authentication.views import login,signup,otp,logout
from authentication.models import User

class SignupTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_signup_get(self):
        response = self.client.get('/authentication/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_post(self):
        response = self.client.post('/authentication/signup/',data = {
            "name" : "dummy",
            "email" : "dhyeypatel1612@gmail.com",
            "phone_number" : "1234567890"
        })
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.all().first().email, "dhyeypatel1612@gmail.com")
        pk = User.objects.all().first().id
        self.assertRedirects(response, '/authentication/otp/'+str(pk)+'/', status_code = 302,target_status_code=200)


class OtpTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(name = "dummy", email = "dhyeypatel189@gmail.com", phone_number = "1234567890")
        self.user.save()

    def test_otp(self):
        response_get = self.client.get('/authentication/otp/'+str(self.user.id)+'/')
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'otp.html')
        otp = User.objects.all().first().otp

        response_post = self.client.post('/authentication/otp/'+str(self.user.id)+'/',data = {
            "otp" : int(otp)
        })
        self.assertRedirects(response_post, '/', status_code = 302, target_status_code = 200)


class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(name = "dummy", email = "dhyey.patel@prodsmiths.com", phone_number = "1234567890")
        self.user.save()

    def test_login_get(self):
        response = self.client.get('/authentication/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post(self):
        response = self.client.post('/authentication/login/',data = {
            "email" : "dhyey.patel@prodsmiths.com"
        })
        self.assertEqual(User.objects.all().count(), 1)
        pk = User.objects.all().first().id
        self.assertRedirects(response, '/authentication/otp/'+str(self.user.id)+'/', status_code = 302,target_status_code=200)
