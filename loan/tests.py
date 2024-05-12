from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Loan
from customer.models import Customer
from apikey.models import APIKey
from django.contrib.auth import get_user_model

class LoanViewTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="test_customer",
            score=1000,
            preapproved_at="2024-05-11T00:00:00Z"
        )
        
        self.customer2 = Customer.objects.create(
            external_id="test_customer2",
            score=2000,
            preapproved_at="2024-05-11T00:00:00Z"
        )

        self.loan = Loan.objects.create(
            external_id="test_loan",
            customer=self.customer,
            amount=500,
            outstanding=400,
            status=1
        )

        user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='password')
        
        self.apikey = APIKey.objects.create(
            key='fgjey3srhdfhgfh3ydhdfh4356h54664fhdghh5h',
            user=user,
        )

    def test_get_loans(self):
        url = reverse('loan_list')
        headers = {'HTTP_API_KEY': self.apikey.key}
        response = self.client.get(url + '?customer_external_id=test_customer', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_loans_missing_param(self):
        url = reverse('loan_list')
        headers = {'HTTP_API_KEY': self.apikey.key}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_loan(self):
        url = reverse('loan_list')
        headers = {'HTTP_API_KEY': self.apikey.key}
        data = {
            'external_id': 'new_loan',
            'customer_external_id': 'test_customer2',
            'amount': 100,
            'outstanding': 50
        }
        response = self.client.post(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_loan_missing_param(self):
        url = reverse('loan_list')
        headers = {'HTTP_API_KEY': self.apikey.key}
        data = {
            'external_id': 'new_loan',
            'customer_external_id': 'test_customer2',
            'amount': 100,
            # Missing 'outstanding' parameter
        }
        response = self.client.post(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_loan_invalid_outstanding(self):
        url = reverse('loan_list')
        headers = {'HTTP_API_KEY': self.apikey.key}
        data = {
            'external_id': 'new_loan',
            'customer_external_id': 'test_customer',
            'amount': 1000,
            'outstanding': 1500
        }
        response = self.client.post(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
