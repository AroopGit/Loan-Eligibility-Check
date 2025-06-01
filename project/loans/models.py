from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from dateutil.relativedelta import relativedelta
import math


class Customer(models.Model):
    """
    Customer model for storing customer information and credit limits.
    """
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(validators=[MinValueValidator(18)])
    monthly_salary = models.PositiveIntegerField()
    approved_limit = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    phone_number = models.CharField(max_length=15)  # Consider using PhoneNumberField
    current_debt = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)

    def calculate_approved_limit(self):
        """
        Calculate the approved limit based on monthly salary.
        Formula: approved_limit = 36 * monthly_salary (rounded to nearest lakh)
        """
        raw_limit = 36 * self.monthly_salary
        return math.ceil(raw_limit / 100000) * 100000

    def update_current_debt(self):
        """
        Update current_debt by summing outstanding amounts of all loans.
        """
        total_debt = self.loans.aggregate(
            total=models.Sum(
                models.F('loan_amount') - models.F('monthly_repayment') * models.F('emis_paid_on_time')
            )
        )['total'] or 0
        self.current_debt = total_debt
        self.save()

    def save(self, *args, **kwargs):
        if not self.approved_limit:
            self.approved_limit = self.calculate_approved_limit()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.customer_id})"


class Loan(models.Model):
    """
    Loan model for storing loan information.
    """
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tenure = models.PositiveIntegerField(help_text="Tenure in months")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual interest rate in percentage")
    monthly_repayment = models.DecimalField(max_digits=15, decimal_places=2)
    emis_paid_on_time = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    date_approved = models.DateTimeField(auto_now_add=True)
    repayments_left = models.PositiveIntegerField()

    def calculate_monthly_repayment(self):
        """
        Calculate EMI using the formula: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
        where P = loan_amount, r = monthly interest rate, n = tenure in months.
        """
        if self.interest_rate == 0:
            return self.loan_amount / self.tenure

        monthly_rate = Decimal(self.interest_rate) / 12 / 100
        tenure = Decimal(self.tenure)
        term = (1 + monthly_rate) ** tenure
        emi = self.loan_amount * monthly_rate * term / (term - 1)
        return emi.quantize(Decimal('0.01'))  # Round to 2 decimal places

    def clean(self):
        if self.emis_paid_on_time > self.tenure:
            raise ValidationError("EMIs paid on time cannot exceed the tenure.")

    def save(self, *args, **kwargs):
        if not self.pk:  # If this is a new loan
            self.repayments_left = self.tenure
            self.monthly_repayment = self.calculate_monthly_repayment()
            self.end_date = self.start_date + relativedelta(months=self.tenure)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan {self.loan_id} for Customer {self.customer.customer_id}"