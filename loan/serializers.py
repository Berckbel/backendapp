from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = (
            "external_id",
            "customer_external_id",
            "amount",
            "outstanding",
            "status",
        )