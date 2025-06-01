import os
import pandas as pd
from datetime import datetime, timedelta
from celery import shared_task
from django.conf import settings
from django.db import transaction
from .models import Customer, Loan


@shared_task
def load_initial_data():
    """
    Background task to load initial customer and loan data from Excel files.
    """
    try:
        # Check if data is already loaded
        if Customer.objects.exists() or Loan.objects.exists():
            print("Data already loaded, skipping initialization...")
            return "Data already loaded, skipping initialization."
        
        # Define file paths
        customer_file = os.path.join(settings.BASE_DIR, 'data', 'customer_data.xlsx')
        loan_file = os.path.join(settings.BASE_DIR, 'data', 'loan_data.xlsx')
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(customer_file), exist_ok=True)
        
        # Check if files exist
        if not os.path.exists(customer_file) or not os.path.exists(loan_file):
            return "Data files not found. Please place the files in the data directory."
        
        # Load customer data
        with transaction.atomic():
            customer_df = pd.read_excel(customer_file)
            
            # Create customer records
            customers = []
            for _, row in customer_df.iterrows():
                customer = Customer(
                    customer_id=row['customer_id'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    phone_number=row['phone_number'],
                    monthly_salary=row['monthly_salary'],
                    approved_limit=row['approved_limit'],
                    current_debt=row.get('current_debt', 0)
                )
                customers.append(customer)
            
            # Bulk create customers
            Customer.objects.bulk_create(customers)
            
            # Load loan data
            loan_df = pd.read_excel(loan_file)
            
            # Create loan records
            loans = []
            for _, row in loan_df.iterrows():
                # Convert date strings to date objects
                start_date = pd.to_datetime(row['start_date']).date() if pd.notna(row['start_date']) else datetime.now().date()
                end_date = pd.to_datetime(row['end_date']).date() if pd.notna(row['end_date']) else (start_date + timedelta(days=30*row['tenure']))
                
                # Calculate repayments left
                tenure = row['tenure']
                emis_paid = row.get('EMIs paid on time', 0)
                repayments_left = max(0, tenure - emis_paid)
                
                loan = Loan(
                    loan_id=row['loan_id'],
                    customer_id=row['customer_id'],
                    loan_amount=row['loan_amount'],
                    tenure=tenure,
                    interest_rate=row['interest_rate'],
                    monthly_repayment=row['monthly_repayment'],
                    emis_paid_on_time=emis_paid,
                    start_date=start_date,
                    end_date=end_date,
                    repayments_left=repayments_left
                )
                loans.append(loan)
            
            # Bulk create loans
            Loan.objects.bulk_create(loans)
        
        return "Successfully loaded initial data"
    
    except Exception as e:
        return f"Error loading initial data: {str(e)}"