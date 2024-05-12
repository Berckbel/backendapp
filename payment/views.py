from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apikey.authentication import APIKeyAuthentication

from .models import Payment, PaymentDetail
from customer.models import Customer
from loan.models import Loan
from .serializers import PaymentSerializer

from decimal import Decimal

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class PaymentView(APIView):

    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get payments for a customer",
        manual_parameters=[
            openapi.Parameter('customer_external_id', openapi.IN_QUERY, description="Customer external ID", type=openapi.TYPE_STRING),
            openapi.Parameter('API-KEY', openapi.IN_HEADER, description="API Key", type=openapi.TYPE_STRING),
        ],
        responses={200: PaymentSerializer(many=True)}
    )
    def get(self, request, format=None):
        try:
            customer_external_id = request.query_params.get('customer_external_id', '')
            
            if not all([customer_external_id]):
                return Response({"error": "all fields are required"}, status=status.HTTP_400_BAD_REQUEST)
            
            customer = Customer.objects.get(external_id=customer_external_id)

            payments = Payment.objects.filter(customer=customer)

            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Customer.DoesNotExist:
            return Response({"error": "customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @swagger_auto_schema(
        operation_description="Create a new payment",
        manual_parameters=[
            openapi.Parameter('API-KEY', openapi.IN_HEADER, description="API Key", type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'external_id': openapi.Schema(type=openapi.TYPE_STRING),
                'customer_external_id': openapi.Schema(type=openapi.TYPE_STRING),
                'loan_external_id': openapi.Schema(type=openapi.TYPE_STRING),
                'payment_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
            },
            required=['external_id', 'customer_external_id', 'loan_external_id', 'payment_amount']
        ),
        responses={200: PaymentSerializer()}
    )
    def post(self, request, format=None):
        try:
            external_id = request.data.get('external_id', '')
            customer_external_id = request.data.get('customer_external_id', '')
            loan_external_id = request.data.get('loan_external_id', '')
            payment_amount = Decimal(request.data.get('payment_amount', 0))

            if not all([external_id, customer_external_id, loan_external_id, payment_amount]):
                return Response({"error": "all fields are required"}, status=status.HTTP_400_BAD_REQUEST)
            
            customer = Customer.objects.get(external_id=customer_external_id)
            loans = Loan.objects.filter(customer=customer, status__in=[1, 2])

            if len(loans) == 0:
                return Response({"error": "no active loans for the user"}, status=status.HTTP_400_BAD_REQUEST)

            loan = Loan.objects.get(external_id=loan_external_id, status__in=[1, 2])
            total_amount = loan.amount

            newPayment = Payment.objects.create(
                external_id = external_id,
                total_amount = total_amount,
                customer = customer,
            )

            loan.outstanding -= payment_amount

            if payment_amount > total_amount:
                newPayment.status = 2
                loan.outstanding += payment_amount
                loan.status = 2

            newPayment.save()

            if loan.outstanding == 0:
                loan.status = 4
            
            loan.save()

            newPaymentDetail = PaymentDetail.objects.create(
                amount = payment_amount,
                loan = loan,
                payment = newPayment,
            )
            newPaymentDetail.save()

            serializer = PaymentSerializer(newPayment, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error": "customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Loan.DoesNotExist:
            return Response({"error": "loan not found"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        