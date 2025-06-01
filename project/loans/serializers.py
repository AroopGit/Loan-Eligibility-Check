from rest_framework import serializers
from .models import Customer, Loan
import math

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name', 'last_name', 'age', 'monthly_salary', 'approved_limit', 'phone_number']

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'age', 'monthly_salary', 'phone_number']
        extra_kwargs = {
            'monthly_salary': {'required': True},
        }

    def create(self, validated_data):
        monthly_salary = validated_data.get('monthly_salary')
        raw_limit = 36 * monthly_salary
        approved_limit = math.ceil(raw_limit / 100000) * 100000
        customer = Customer.objects.create(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            age=validated_data.get('age'),
            monthly_salary=monthly_salary,
            approved_limit=approved_limit,
            phone_number=validated_data.get('phone_number'),
            current_debt=0
        )
        return customer

class CustomerResponseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['customer_id', 'name', 'age', 'monthly_salary', 'approved_limit', 'phone_number']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class LoanEligibilityRequestSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()

class LoanEligibilityResponseSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    approval = serializers.BooleanField()
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    corrected_interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()
    monthly_installment = serializers.DecimalField(max_digits=15, decimal_places=2)

class LoanCreationRequestSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()

class LoanCreationResponseSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField(allow_null=True)
    customer_id = serializers.IntegerField()
    loan_approved = serializers.BooleanField()
    message = serializers.CharField(allow_blank=True)
    monthly_installment = serializers.DecimalField(max_digits=15, decimal_places=2)

class LoanDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Loan
        fields = ['loan_id', 'customer', 'loan_amount', 'interest_rate', 'monthly_repayment', 'tenure']

class LoanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['loan_id', 'loan_amount', 'interest_rate', 'monthly_repayment', 'repayments_left']