import math
from decimal import Decimal
from datetime import datetime, date
from django.db.models import Sum, Q
from .models import Loan


def calculate_credit_score(customer):
    """
    Calculate credit score (out of 100) for a customer based on their loan history.
    
    Components:
    1. Past Loans paid on time
    2. No of loans taken in past
    3. Loan activity in current year
    4. Loan approved volume
    5. Current loans > approved limit
    """
    loans = Loan.objects.filter(customer=customer)
    
    # If no loan history, assign a default moderate score
    if not loans.exists():
        return 50
    
    # Component 1: Past Loans paid on time (30 points)
    total_emis = sum(loan.tenure for loan in loans)
    total_emis_paid_on_time = sum(loan.emis_paid_on_time for loan in loans)
    
    on_time_ratio = total_emis_paid_on_time / total_emis if total_emis > 0 else 0
    on_time_score = min(30, int(on_time_ratio * 30))
    
    # Component 2: Number of loans taken in past (15 points)
    # More loans means more history, which can be good up to a point
    num_loans = loans.count()
    loan_count_score = min(15, num_loans * 3)
    
    # Component 3: Loan activity in current year (20 points)
    # Recent activity shows current creditworthiness
    current_year = datetime.now().year
    current_year_loans = loans.filter(
        Q(start_date__year=current_year) | Q(end_date__year=current_year)
    )
    current_year_score = min(20, current_year_loans.count() * 5)
    
    # Component 4: Loan approved volume (20 points)
    # Higher approved volumes show trust from lenders
    total_loan_amount = loans.aggregate(total=Sum('loan_amount'))['total'] or Decimal('0')
    # Scale: 0-100k: 5pts, 100k-500k: 10pts, 500k-1M: 15pts, >1M: 20pts
    volume_score = 0
    if total_loan_amount > Decimal('1000000'):
        volume_score = 20
    elif total_loan_amount > Decimal('500000'):
        volume_score = 15
    elif total_loan_amount > Decimal('100000'):
        volume_score = 10
    elif total_loan_amount > Decimal('0'):
        volume_score = 5
    
    # Component 5: Current loans > approved limit (15 points)
    # Check if sum of current loans exceeds approved limit
    current_loans = loans.filter(end_date__gte=date.today())
    current_debt = current_loans.aggregate(total=Sum('loan_amount'))['total'] or Decimal('0')
    
    limit_score = 15
    if current_debt > customer.approved_limit:
        limit_score = 0
    
    # Sum all components for final score
    credit_score = on_time_score + loan_count_score + current_year_score + volume_score + limit_score
    
    return credit_score


def calculate_monthly_installment(loan_amount, interest_rate, tenure):
    """
    Calculate monthly installment using compound interest formula.
    
    Args:
        loan_amount: Loan amount (decimal)
        interest_rate: Annual interest rate in percentage (decimal)
        tenure: Loan tenure in months (int)
        
    Returns:
        Monthly installment amount (decimal)
    """
    # Convert annual interest rate to monthly decimal rate
    monthly_rate = Decimal(interest_rate) / Decimal('100') / Decimal('12')
    
    # Convert loan amount to decimal if it's not already
    loan_amount = Decimal(loan_amount)
    
    # Calculate using compound interest formula: P * r * (1 + r)^n / ((1 + r)^n - 1)
    if monthly_rate == 0:
        # If interest rate is 0, simply divide loan amount by tenure
        return loan_amount / Decimal(tenure)
    
    numerator = loan_amount * monthly_rate * (1 + monthly_rate) ** tenure
    denominator = (1 + monthly_rate) ** tenure - 1
    
    monthly_installment = numerator / denominator
    
    # Round to 2 decimal places
    return monthly_installment.quantize(Decimal('0.01'))


def determine_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    """
    Determine if a customer is eligible for a loan based on credit score and other factors.
    
    Returns:
        tuple: (approval, corrected_interest_rate, monthly_installment)
    """
    # Calculate credit score
    credit_score = calculate_credit_score(customer)
    
    # Calculate total EMIs of current loans
    current_loans = Loan.objects.filter(
        customer=customer, 
        end_date__gte=date.today()
    )
    total_emi = current_loans.aggregate(Sum('monthly_repayment'))['monthly_repayment__sum'] or Decimal('0')
    
    # Calculate monthly installment
    monthly_installment = calculate_monthly_installment(loan_amount, interest_rate, tenure)
    
    # Check if sum of all current EMIs > 50% of monthly salary
    if total_emi + monthly_installment > (Decimal(customer.monthly_salary) * Decimal('0.5')):
        return False, interest_rate, monthly_installment
    
    # Determine approval and corrected interest rate based on credit score
    if credit_score > 50:
        # Approve loan with original interest rate
        return True, interest_rate, monthly_installment
    
    elif 30 < credit_score <= 50:
        # Approve loan but ensure interest rate >= 12%
        corrected_rate = max(Decimal('12.0'), Decimal(interest_rate))
        if corrected_rate > interest_rate:
            # Recalculate monthly installment with corrected rate
            monthly_installment = calculate_monthly_installment(loan_amount, corrected_rate, tenure)
        return True, corrected_rate, monthly_installment
    
    elif 10 < credit_score <= 30:
        # Approve loan but ensure interest rate >= 16%
        corrected_rate = max(Decimal('16.0'), Decimal(interest_rate))
        if corrected_rate > interest_rate:
            # Recalculate monthly installment with corrected rate
            monthly_installment = calculate_monthly_installment(loan_amount, corrected_rate, tenure)
        return True, corrected_rate, monthly_installment
    
    else:
        # Don't approve any loans
        return False, interest_rate, monthly_installment