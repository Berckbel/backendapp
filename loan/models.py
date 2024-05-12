from django.db import models
from customer.models import Customer

# Create your models here.
class Loan(models.Model):
    external_id = models.CharField(unique=True, max_length=60)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.IntegerField(choices=(
        (1, 'pending'),
        (2, 'active'),
        (3, 'rejected'),
        (4, 'paid'),
    ), default=1)

    contract_version = models.TextField(null=True, blank=True, max_length=30)

    maximum_payment_date = models.DateTimeField(null=True, blank=True)
    taken_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    customer = models.ForeignKey(Customer, related_name="customer_loan", on_delete=models.CASCADE)

    outstanding = models.DecimalField(blank=False, null=False, max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=False, auto_now=True)

    def customer_external_id(self):
        return self.customer.external_id
    
    def __str__(self):
        return self.external_id