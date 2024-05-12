from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apikey.authentication import APIKeyAuthentication

from django.db.utils import IntegrityError

from .models import Loan
from customer.models import Customer
from .serializers import LoanSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class LoanView(APIView):

    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get loans for a customer",
        manual_parameters=[
            openapi.Parameter('customer_external_id', openapi.IN_QUERY, description="Customer external ID", type=openapi.TYPE_STRING),
            openapi.Parameter('API-KEY', openapi.IN_HEADER, description="API Key", type=openapi.TYPE_STRING),
        ],
        responses={200: LoanSerializer(many=True)}
    )
    def get(self, request, format=None):
        try:
            customer_external_id = request.query_params.get('customer_external_id', '')

            if not all([customer_external_id]):
                return Response({"error": "all fields are required"}, status=status.HTTP_400_BAD_REQUEST)

            customer = Customer.objects.get(external_id=customer_external_id)
            loans = Loan.objects.filter(customer=customer, status__in=[1, 2])

            serializer = LoanSerializer(loans, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Customer.DoesNotExist:
            return Response({"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_description="Create a new loan",
         manual_parameters=[
            openapi.Parameter('API-KEY', openapi.IN_HEADER, description="API Key", type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'external_id': openapi.Schema(type=openapi.TYPE_STRING),
                'customer_external_id': openapi.Schema(type=openapi.TYPE_STRING),
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
                'outstanding': openapi.Schema(type=openapi.TYPE_NUMBER),
            },
            required=['external_id', 'customer_external_id', 'amount', 'outstanding']
        ),
        responses={200: LoanSerializer()}
    )
    def post(self, request, format=None):
        try:
            external_id = request.data.get('external_id', '')
            customer_external_id = request.data.get('customer_external_id', '')
            amount = float(request.data.get('amount', 0))
            outstanding = float(request.data.get('outstanding', 0))

            if not all([external_id, customer_external_id, amount, outstanding]):
                return Response({"error": "all fields are required"}, status=status.HTTP_400_BAD_REQUEST)
            
            customer = Customer.objects.get(external_id=customer_external_id)

            if outstanding > customer.score:
                return Response({"error": "the outstanding must be lower than the score"}, status=status.HTTP_400_BAD_REQUEST)

            newLoan = Loan.objects.create(
                external_id = external_id,
                customer = customer,
                amount = amount,
                outstanding = outstanding,
            )
            
            newLoan.status = 2

            newLoan.save()

            serializer = LoanSerializer(newLoan, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Customer.DoesNotExist:
            return Response({"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"error": "id keys must be unique"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        