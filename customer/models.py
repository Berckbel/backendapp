from django.db import models

# Create your models here.
class Customer(models.Model):
    external_id = models.CharField(unique=True, max_length=60)
    score = models.DecimalField(null=False, blank=False, max_digits=12, decimal_places=2)

    status = models.IntegerField(choices=(
        (1, 'Active'),
        (2, 'Inactive'),
    ), default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=False, auto_now=True)

    preapproved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.external_id