from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "external_id",
            "status",
            "score",
            "preapproved_at",
        )

class CustomerBalanceSerializer(serializers.Serializer):
    class Meta:
        model = Customer
        fields = (
            "external_id",
            "score",
            "available_amount",
            "total_debt",
        )