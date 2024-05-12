from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from apikey.authentication import APIKeyAuthentication

from .models import Customer
from loan.models import Loan
from .serializers import CustomerSerializer

from decimal import Decimal

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class CustomerView(APIView):

    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get customer details",
        manual_parameters=[
            openapi.Parameter('external_id', openapi.IN_QUERY, description="Customer external ID", type=openapi.TYPE_STRING),
            openapi.Parameter('API-KEY', openapi.IN_HEADER, description="API Key", type=openapi.TYPE_STRING),
        ],
        responses={200: CustomerSerializer()}
    )
    def get(self, request, format=None):
        try:
            external_id = request.query_params.get('external_id', '')

            if not all([external_id]):
                return Response({"error": "all fields are required"}, status=status.HTTP_400_BAD_REQUEST)

            customer = Customer.objects.get(external_id=external_id)

            serializer = CustomerSerializer(customer, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @swagger_auto_schema(
        operation_description="Create a new customer",
        manual_parameters=[
            openapi.Parameter('API-KEY', openapi.IN_HEADER, description="API Key", type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'external_id': openapi.Schema(type=openapi.TYPE_STRING),
                'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                'score': openapi.Schema(type=openapi.TYPE_NUMBER),
                'preapproved_at': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['external_id', 'status', 'score', 'preapproved_at']
        ),
        responses={200: CustomerSerializer()}
    )
    def post(self, request, format=None):
        try:

            external_id = request.data.get('external_id', '')
            status_data = int(request.data.get('status', 1))
            score = Decimal(request.data.get('score', 0))
            preapproved_at = request.data.get('preapproved_at', '')

            if not all([external_id, status_data, score, preapproved_at]):
                return Response({"error": "all fields are required"}, status=status.HTTP_400_BAD_REQUEST)

            newCustomer = Customer.objects.create(
                external_id = external_id,
                status = status_data,
                score = score,
                preapproved_at = preapproved_at
            )

            newCustomer.save()

            serializer = CustomerSerializer(newCustomer, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@swagger_auto_schema(
    method='GET',
    operation_description="Get the balance for a customer",
    manual_parameters=[
        openapi.Parameter('external_id', openapi.IN_QUERY, description="Customer external ID", type=openapi.TYPE_STRING),
        openapi.Parameter('API-KEY', openapi.IN_HEADER, description="API Key", type=openapi.TYPE_STRING),
    ],
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'external_id': openapi.Schema(type=openapi.TYPE_STRING),
            'score': openapi.Schema(type=openapi.TYPE_NUMBER),
            'available_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
            'total_debt': openapi.Schema(type=openapi.TYPE_NUMBER),
        }
    )}
)
@api_view(['GET'])
@authentication_classes([APIKeyAuthentication])
@permission_classes([IsAuthenticated])
def getCustomerBalance(request):
    try:
        external_id = request.query_params.get('external_id', '')

        if not all([external_id]):
            return Response({"error": "all fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        customer = Customer.objects.get(external_id=external_id)
        loans = Loan.objects.filter(customer=customer)

        balance = {
            'external_id': customer.external_id,
            'score': customer.score,
            'available_amount': 0,
            'total_debt': 0,
        }

        for loan in loans:
            balance['total_debt'] += loan.outstanding
            
        balance['available_amount'] = balance['score'] - balance['total_debt']

        return Response(balance, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)