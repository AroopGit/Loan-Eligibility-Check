from django.urls import path
from .views import (
    CustomerRegistrationView,
    LoanEligibilityView,
    LoanCreationView,
    LoanDetailView,
    CustomerLoansView
)

urlpatterns = [
    path('register', CustomerRegistrationView.as_view(), name='register'),
    path('check-eligibility', LoanEligibilityView.as_view(), name='check-eligibility'),
    path('create-loan', LoanCreationView.as_view(), name='create-loan'),
    path('view-loan/<int:loan_id>', LoanDetailView.as_view(), name='view-loan'),
    path('view-loans/<int:customer_id>', CustomerLoansView.as_view(), name='view-loans'),
]