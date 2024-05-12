from rest_framework import serializers
from .models import Payment, PaymentDetail

class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = (
            "loan_external_id",
            "payment_amount",
        )

class PaymentSerializer(serializers.ModelSerializer):
    payment_details = PaymentDetailSerializer(many=True, read_only=True, source='payment_payment_detail')

    class Meta:
        model = Payment
        fields = (
            "external_id",
            "customer_external_id",
            "payment_date",
            "status",
            "total_amount",
            "payment_details"
        )


