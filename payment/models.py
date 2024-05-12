from django.db import models
from customer.models import Customer
from loan.models import Loan

# Create your models here.
class Payment(models.Model):
    external_id = models.CharField(unique=True, max_length=255)
    total_amount = models.DecimalField(blank=False, null=False, max_digits=20, decimal_places=10)

    status = models.IntegerField(choices=(
        (1, 'completed'),
        (2, 'rejected'),
    ), default=1)

    paid_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(Customer, related_name="customer_payment", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=False, auto_now=True)

    def __str__(self):
        return self.external_id
    
    def customer_external_id(self):
        return self.customer.external_id
    
    def payment_date(self):
        return self.paid_at

class PaymentDetail(models.Model):
    amount = models.DecimalField(blank=False, null=False, max_digits=20, decimal_places=10)

    loan = models.ForeignKey(Loan, related_name="loan_payment_detail", on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, related_name="payment_payment_detail", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=False, auto_now=True)

    def __str__(self):
        return self.created_at
    
    def payment_amount(self):
        return self.amount
    
    def loan_external_id(self):
        return self.loan.external_id
