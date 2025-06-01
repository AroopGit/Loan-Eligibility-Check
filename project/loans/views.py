from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date, timedelta
from decimal import Decimal
from django.shortcuts import get_object_or_404
from .models import Customer, Loan
from .serializers import (
    CustomerRegistrationSerializer,
    CustomerResponseSerializer,
    LoanEligibilityRequestSerializer,
    LoanEligibilityResponseSerializer,
    LoanCreationRequestSerializer,
    LoanCreationResponseSerializer,
    LoanDetailSerializer,
    LoanListSerializer
)
from .utils import calculate_credit_score, calculate_monthly_installment, determine_loan_eligibility


class CustomerRegistrationView(APIView):
    """
    API endpoint for customer registration.
    """
    def post(self, request, *args, **kwargs):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            response_serializer = CustomerResponseSerializer(customer)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanEligibilityView(APIView):
    """
    API endpoint to check loan eligibility.
    """
    def post(self, request, *args, **kwargs):
        serializer = LoanEligibilityRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            try:
                customer = Customer.objects.get(customer_id=data['customer_id'])
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Determine loan eligibility
            approval, corrected_interest_rate, monthly_installment = determine_loan_eligibility(
                customer, 
                data['loan_amount'], 
                data['interest_rate'], 
                data['tenure']
            )
            
            response_data = {
                'customer_id': customer.customer_id,
                'approval': approval,
                'interest_rate': data['interest_rate'],
                'corrected_interest_rate': corrected_interest_rate,
                'tenure': data['tenure'],
                'monthly_installment': monthly_installment
            }
            
            response_serializer = LoanEligibilityResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            return Response(response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanCreationView(APIView):
    """
    API endpoint to process a new loan application.
    """
    def post(self, request, *args, **kwargs):
        serializer = LoanCreationRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            try:
                customer = Customer.objects.get(customer_id=data['customer_id'])
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Determine loan eligibility
            approval, corrected_interest_rate, monthly_installment = determine_loan_eligibility(
                customer, 
                data['loan_amount'], 
                data['interest_rate'], 
                data['tenure']
            )
            
            response_data = {
                'customer_id': customer.customer_id,
                'loan_approved': False,
                'message': '',
                'monthly_installment': monthly_installment,
                'loan_id': None
            }
            
            if not approval:
                response_data['message'] = 'Loan not approved. Credit score too low or EMI exceeds 50% of monthly salary.'
            else:
                # Create the loan
                start_date = date.today()
                end_date = start_date + timedelta(days=30 * data['tenure'])
                
                loan = Loan.objects.create(
                    customer=customer,
                    loan_amount=data['loan_amount'],
                    interest_rate=corrected_interest_rate,
                    tenure=data['tenure'],
                    monthly_repayment=monthly_installment,
                    start_date=start_date,
                    end_date=end_date,
                    repayments_left=data['tenure']
                )
                
                response_data['loan_approved'] = True
                response_data['loan_id'] = loan.loan_id
                
                # Update customer's current debt
                customer.current_debt += Decimal(data['loan_amount'])
                customer.save()
            
            response_serializer = LoanCreationResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_201_CREATED if approval else status.HTTP_200_OK)
            return Response(response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanDetailView(APIView):
    """
    API endpoint to view loan details by loan_id.
    """
    def get(self, request, loan_id, *args, **kwargs):
        loan = get_object_or_404(Loan, loan_id=loan_id)
        serializer = LoanDetailSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerLoansView(APIView):
    """
    API endpoint to view all loans by customer_id.
    """
    def get(self, request, customer_id, *args, **kwargs):
        # Check if customer exists
        get_object_or_404(Customer, customer_id=customer_id)
        
        # Get all loans for the customer
        loans = Loan.objects.filter(customer_id=customer_id)
        
        if not loans.exists():
            return Response([], status=status.HTTP_200_OK)
        
        serializer = LoanListSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)