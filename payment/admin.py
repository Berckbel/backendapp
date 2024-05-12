from django.contrib import admin
from .models import Payment, PaymentDetail

# Register your models here.
admin.site.register(Payment)
admin.site.register(PaymentDetail)