from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Customer
from apikey.models import APIKey
from django.contrib.auth import get_user_model

class CustomerViewTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="test_customer",
            score=500,
            preapproved_at="2024-05-11T00:00:00Z"
        )
        
        user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='password')
        
        self.apikey = APIKey.objects.create(
            key='1524652fsgtewrgdfsbdfsgw5234',
            user=user,
        )

    def test_get_customer(self):
        url = reverse('customer_balance')
        headers = {'HTTP_API_KEY': self.apikey.key}
        response = self.client.get(url + '?external_id=test_customer', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customer_not_found(self):
        url = reverse('customer_balance')
        headers = {'HTTP_API_KEY': self.apikey.key}
        response = self.client.get(url + '?external_id=non_existent_customer', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_customer(self):
        url = reverse('customer_list')
        headers = {'HTTP_API_KEY': self.apikey.key}
        data = {
            'external_id': 'new_customer',
            'status': 2,
            'score': 600,
            'preapproved_at': '2024-05-12T00:00:00Z'
        }
        response = self.client.post(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
