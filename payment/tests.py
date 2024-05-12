from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Payment, PaymentDetail
from customer.models import Customer
from loan.models import Loan
from apikey.models import APIKey
from django.contrib.auth import get_user_model

class PaymentViewTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            external_id="test_customer",
            score=1000,
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
            key='adfsoajsfdsfn4387fvkjsdgdursg',
            user=user,
        )

    def test_get_payments(self):
        url = reverse('payment_list')
        headers = {'HTTP_API_KEY': self.apikey.key}
        response = self.client.get(url + '?customer_external_id=test_customer', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_payments_missing_param(self):
        url = reverse('payment_list')
        headers = {'HTTP_API_KEY': self.apikey.key}
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_payment(self):
        url = reverse('payment_list')
        headers = {'HTTP_API_KEY': self.apikey.key}
        data = {
            'external_id': 'new_payment',
            'customer_external_id': 'test_customer',
            'loan_external_id': 'test_loan',
            'payment_amount': 100
        }
        response = self.client.post(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_payment_missing_param(self):
        url = reverse('payment_list')
        headers = {'HTTP_API_KEY': self.apikey.key}
        data = {
            'external_id': 'new_payment',
            'customer_external_id': 'test_customer',
            'loan_external_id': 'test_loan',
            # Missing 'payment_amount' parameter
        }
        response = self.client.post(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_payment_invalid_loan(self):
        url = reverse('payment_list')
        headers = {'HTTP_API_KEY': self.apikey.key}
        data = {
            'external_id': 'new_payment',
            'customer_external_id': 'test_customer',
            'loan_external_id': 'invalid_loan',
            'payment_amount': 100
        }
        response = self.client.post(url, data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
