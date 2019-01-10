from django.test import TestCase
from rest_framework.test import APIRequestFactory
from apis.v1.views import RegisterDevice, Login
from rest_framework import status
from apps.models import Device
from django.contrib.auth.models import User

# Create your tests here.


class TestRegisterDevice(TestCase):

    def setUp(self):
        # self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = RegisterDevice.as_view()

    def tearDown(self):
        Device.objects.get(user=User.objects.get(username='01728709288')).delete()

    def test_register_device(self):
        data = {
                  "username": "01728709288",
                  "shop_name": "Test Shop Name",
                  "pin": "1234"
                }
        request = self.factory.post('/apis/v1/register/', data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestLogin(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        # self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = Login.as_view()

    def test_login(self):
        data = {
                  "username": "01913563376",
                  "pin": "1234"
                }
        request = self.factory.post('/apis/v1/login/', data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestChangePin(TestCase):
    pass

class TestCategory(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        # self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = Login.as_view()