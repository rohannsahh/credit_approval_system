import pandas as pd
# from credit_approval.celery_app import shared_task

from celery import shared_task
from .models import Customer, Loan

@shared_task
def load_customer_data():
    file_path = 'data/customer_data.xlsx'
    data = pd.read_excel(file_path)
    for _, row in data.iterrows():
        Customer.objects.update_or_create(
            customer_id=row['customer_id'],
            defaults={
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'phone_number': row['phone_number'],
                'monthly_salary': row['monthly_salary'],
                'approved_limit': row['approved_limit'],
                'current_debt': row['current_debt']
            }
        )

@shared_task
def load_loan_data():
    file_path = 'data/loan_data.xlsx'
    data = pd.read_excel(file_path)
    for _, row in data.iterrows():
        Loan.objects.update_or_create(
            loan_id=row['loan_id'],
            defaults={
                'customer_id': row['customer_id'],
                'loan_amount': row['loan_amount'],
                'tenure': row['tenure'],
                'interest_rate': row['interest_rate'],
                'monthly_repayment': row['monthly_repayment'],
                'emis_paid_on_time': row['emis_paid_on_time'],
                'start_date': row['start_date'],
                'end_date': row['end_date']
            }
        )
