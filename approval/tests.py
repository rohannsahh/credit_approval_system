# from django.test import TestCase

# # Create your tests here.
# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from django.utils import timezone
# from .models import Customer, Loan
# from decimal import Decimal
# from datetime import timedelta

# class APITestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
        
#         # Create a test customer
#         self.customer = Customer.objects.create(
#             first_name="Johnn",
#             last_name="Doen",
#             phone_number="1230567890",
#             age=30,
#             monthly_salary=50000,
#             approved_limit=1000000,
#             current_debt=0
#         )

#         # Create a test loan
#         self.loan = Loan.objects.create(
#             customer=self.customer,
#             loan_amount=50000,
#             interest_rate=10.5,
#             tenure=12,
#             monthly_repayment=Decimal("4166.67"),
#             emis_paid_on_time=10,
#             start_date=timezone.now().date(),
#             end_date=timezone.now().date() + timedelta(days=365)
#         )




# class RegisterCustomerTest(APITestCase):
#     def test_register_customer(self):
#         data = {
#             "first_name": "Janegtr",
#             "last_name": "Dotgte",
#             "phone_number": "9980854321",
#             "age": 28,
#             "monthly_income": 40000
#         }
#         response = self.client.post('api/register-customer/', data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn("approved_limit", response.data)
#         self.assertEqual(response.data["first_name"], "Janegtr")


# class CheckEligibilityTest(APITestCase):
#     def test_check_eligibility(self):
#         data = {
#             "customer_id": self.customer.customer_id,
#             "loan_amount": 100000,
#             "interest_rate": 12,
#             "tenure": 24
#         }
#         response = self.client.post('api/check-eligibility/', data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("approval", response.data)

# class CreateLoanTest(APITestCase):
#     def test_create_loan(self):
#         data = {
#             "customer_id": self.customer.customer_id,
#             "loan_amount": 100000,
#             "interest_rate": 10.5,
#             "tenure": 24
#         }
#         response = self.client.post('api/create-loan/', data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(response.data["loan_approved"])
#         self.assertIn("loan_id", response.data)

# class ViewLoanTest(APITestCase):
#     def test_view_loan(self):
#         response = self.client.get(f'api/view-loan/{self.loan.loan_id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["loan_id"], self.loan.loan_id)
#         self.assertEqual(response.data["customer"]["id"], self.customer.customer_id)

# class ViewLoansTest(APITestCase):
#     def test_view_loans(self):
#         response = self.client.get(f'api/view-loans/{self.customer.customer_id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(len(response.data) > 0)
#         self.assertEqual(response.data[0]["loan_id"], self.loan.loan_id)



from django.test import TestCase

# # Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from .models import Customer, Loan
from decimal import Decimal
from datetime import timedelta

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create a test customer
        self.customer = Customer.objects.create(
            first_name="Johnn",
            last_name="Doen",
            phone_number="1230567890",
            age=30,
            monthly_salary=50000,
            approved_limit=1000000,
            current_debt=0
        )

        # Create a test loan
        self.loan = Loan.objects.create(
            customer=self.customer,
            loan_amount=50000,
            interest_rate=10.5,
            tenure=12,
            monthly_repayment=Decimal("4166.67"),
            emis_paid_on_time=10,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=365)
        )




class RegisterCustomerTest(APITestCase):
    def test_register_customer(self):
        data = {
            "first_name": "Janegtr",
            "last_name": "Dotgte",
            "phone_number": "9980854321",
            "age": 28,
            "monthly_income": 40000
        }
        response = self.client.post('/api/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("approved_limit", response.data)
        self.assertEqual(response.data["first_name"], "Janegtr")


class CheckEligibilityTest(APITestCase):
    def test_check_eligibility(self):
        data = {
            "customer_id": self.customer.customer_id,
            "loan_amount": 100000,
            "interest_rate": 12,
            "tenure": 24
        }
        response = self.client.post('/api/check-eligibility/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("approval", response.data)

class CreateLoanTest(APITestCase):
    def test_create_loan(self):
        data = {
            "customer_id": self.customer.customer_id,
            "loan_amount": 100000,
            "interest_rate": 10.5,
            "tenure": 24
        }
        response = self.client.post('/api/create-loan/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["loan_approved"])
        self.assertIn("loan_id", response.data)

class ViewLoanTest(APITestCase):
    def test_view_loan(self):
        response = self.client.get(f'/api/view-loan/{self.loan.loan_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["loan_id"], self.loan.loan_id)
        self.assertEqual(response.data["customer"]["id"], self.customer.customer_id)

class ViewLoansTest(APITestCase):
    def test_view_loans(self):
        response = self.client.get(f'/api/view-loans/{self.customer.customer_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.data[0]["loan_id"], self.loan.loan_id)

