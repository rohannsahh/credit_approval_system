from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer
from django.db.models import Sum
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta


class RegisterCustomer(APIView):
    def post(self, request):
        data = request.data
        monthly_income = data.get("monthly_income")

        # Calculate the approved limit based on the monthly income
        approved_limit = round(36 * monthly_income / 100000) * 100000

        # Prepare customer data
        customer_data = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "phone_number": data["phone_number"],
            "age": data["age"],
            "monthly_salary": monthly_income,
            "approved_limit": approved_limit,
            "current_debt": 0,  # Set initial debt to 0 for a new customer
        }

        # Use serializer to validate and save data
        serializer = CustomerSerializer(data=customer_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CheckEligibility(APIView):
    def post(self, request):
        customer_id = request.data.get("customer_id")
        loan_amount = request.data.get("loan_amount")
        interest_rate = request.data.get("interest_rate")
        tenure = request.data.get("tenure")

        try:
            # Get the customer record
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Step 1: Calculate credit score based on loan history
        loans = Loan.objects.filter(customer_id=customer_id)
        total_loan_amount = loans.aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0
        on_time_emis = loans.aggregate(Sum('emis_paid_on_time'))['emis_paid_on_time__sum'] or 0
        total_loans_count = loans.count()

        # Initial credit score based on past payments
        credit_score = 50
        if total_loan_amount > customer.approved_limit:
            credit_score = 0  # Exceeding approved limit sets score to 0
        else:
            if on_time_emis >= total_loans_count * 0.8:  # 80% EMIs paid on time
                credit_score += 20
            if total_loans_count < 5:
                credit_score += 10
            if total_loans_count >= 5 and on_time_emis < total_loans_count * 0.5:
                credit_score -= 20

        # Step 2: Determine eligibility based on credit score and other rules
        approved = False
        corrected_interest_rate = interest_rate  # Default to provided rate
        monthly_income = customer.monthly_salary
        if credit_score > 50:
            approved = True
        elif 30 < credit_score <= 50:
            if interest_rate <= 12:
                corrected_interest_rate = 12  # Adjust minimum interest rate
            approved = True
        elif 10 < credit_score <= 30:
            if interest_rate <= 16:
                corrected_interest_rate = 16
            approved = True
        elif credit_score <= 10:
            approved = False  # Low score, reject loan

        # Check for monthly EMI constraint
        if approved:
            monthly_installment = loan_amount / tenure
            if monthly_installment > Decimal(0.5) * monthly_income:
                approved = False  # Exceeds 50% of monthly income

        # Step 3: Prepare the response
        response_data = {
            "customer_id": customer_id,
            "approval": approved,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_interest_rate,
            "tenure": tenure,
            "monthly_installment": loan_amount / tenure if approved else 0
        }

        return Response(response_data, status=status.HTTP_200_OK)





class CreateLoan(APIView):
    def post(self, request):
        customer_id = request.data.get("customer_id")
        loan_amount = Decimal(request.data.get("loan_amount"))
        interest_rate = Decimal(request.data.get("interest_rate"))
        tenure = int(request.data.get("tenure"))

        try:
            # Fetch the customer data
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check eligibility conditions
        existing_loans = Loan.objects.filter(customer_id=customer_id)
        total_existing_loan_amount = existing_loans.aggregate(total=Sum('loan_amount'))['total'] or Decimal(0)
        monthly_income = customer.monthly_salary

        if total_existing_loan_amount + loan_amount > customer.approved_limit:
            return Response({
                "loan_id": None,
                "customer_id": customer_id,
                "loan_approved": False,
                "message": "Loan exceeds approved limit."
            }, status=status.HTTP_400_BAD_REQUEST)

        monthly_installment = loan_amount / tenure
        if monthly_installment > Decimal(0.5) * monthly_income:
            return Response({
                "loan_id": None,
                "customer_id": customer_id,
                "loan_approved": False,
                "message": "Monthly installment exceeds 50% of monthly salary."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Set default start and end dates if not provided
        start_date = request.data.get("start_date", timezone.now().date())
        end_date = start_date + timedelta(days=tenure * 30)  # Approximating 1 month as 30 days

        # Approve and create the loan
        with transaction.atomic():
            loan = Loan.objects.create(
                customer=customer,
                loan_amount=loan_amount,
                interest_rate=interest_rate,
                tenure=tenure,
                monthly_repayment=monthly_installment,
                emis_paid_on_time=0,
                start_date=start_date,
                end_date=end_date
            )

        response_data = {
            "loan_id": loan.loan_id,
            "customer_id": customer.customer_id,
            "loan_approved": True,
            "message": "Loan approved successfully",
            "monthly_installment": monthly_installment,
            "start_date": start_date,
            "end_date": end_date
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    

class ViewLoan(APIView):
     def get(self, request, loan_id):
        try:
            # Retrieve the loan and related customer information
            loan = Loan.objects.select_related('customer').get(loan_id=loan_id)
            customer = loan.customer
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND)

        # Prepare the response data
        response_data = {
            "loan_id": loan.loan_id,
            "customer": {
                "id": customer.customer_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "phone_number": customer.phone_number,
                "age": customer.age,  # Ensure 'age' is a field in Customer model
            },
            "loan_approved": True,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_repayment,
            "tenure": loan.tenure
        }
        return Response(response_data, status=status.HTTP_200_OK)
     
class ViewLoans(APIView):
     def get(self, request, customer_id):
        # Fetch all loans related to the customer_id
        loans = Loan.objects.filter(customer_id=customer_id)

        # Check if loans are found
        if not loans.exists():
            return Response({"error": "No loans found for this customer."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize loan data
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

