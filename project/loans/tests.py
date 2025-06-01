from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Customer, Loan
from datetime import date, timedelta

class CustomerRegistrationTests(APITestCase):
    def test_customer_registration(self):
        """Test customer registration endpoint"""
        url = reverse('register')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'monthly_income': 50000,
            'phone_number': '1234567890'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(response.data['approved_limit'], 1800000)  # 36 * 50000

class LoanEligibilityTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            age=30,
            monthly_salary=50000,
            phone_number='1234567890',
            approved_limit=1800000
        )

    def test_loan_eligibility_check(self):
        """Test loan eligibility check endpoint"""
        url = reverse('check-eligibility')
        data = {
            'customer_id': self.customer.customer_id,
            'loan_amount': 100000,
            'interest_rate': 12.5,
            'tenure': 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('approval', response.data)
        self.assertIn('monthly_installment', response.data)

class LoanCreationTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            age=30,
            monthly_salary=50000,
            phone_number='1234567890',
            approved_limit=1800000
        )

    def test_loan_creation(self):
        """Test loan creation endpoint"""
        url = reverse('create-loan')
        data = {
            'customer_id': self.customer.customer_id,
            'loan_amount': 100000,
            'interest_rate': 12.5,
            'tenure': 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['loan_approved'])
        self.assertIsNotNone(response.data['loan_id'])

class LoanViewTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            age=30,
            monthly_salary=50000,
            phone_number='1234567890',
            approved_limit=1800000
        )
        self.loan = Loan.objects.create(
            customer=self.customer,
            loan_amount=100000,
            interest_rate=12.5,
            tenure=12,
            monthly_repayment=8884.88,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=365),
            repayments_left=12
        )

    def test_view_loan_details(self):
        """Test viewing individual loan details"""
        url = reverse('view-loan', args=[self.loan.loan_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['loan_id'], self.loan.loan_id)

    def test_view_customer_loans(self):
        """Test viewing all loans for a customer"""
        url = reverse('view-loans', args=[self.customer.customer_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)