import os
import django
import base64
import json
import requests
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tantawy.settings')
django.setup()

from core.models import Agent, CustomerVendor, VisitPlan, Transaction, Store, InvoiceMaster, Account
from django.contrib.auth.models import User
from django.test import RequestFactory
from authentication.views import customer_transactions_api

import sys

def test_endpoint():
    try:
        sys.stdout.write("Setting up test data...\n")
        sys.stdout.flush()
        
        # Create a test user
        sys.stdout.write("Creating user...\n")
        sys.stdout.flush()
        user, _ = User.objects.get_or_create(username='test_admin', defaults={'is_superuser': True})
        
        # Create a test store
        sys.stdout.write("Creating store...\n")
        sys.stdout.flush()
        customer1, _ = CustomerVendor.objects.get_or_create(
            customerVendorName='Test Customer 1',
            defaults={'type': 1, 'createdBy': user}
        )
        customer2, _ = CustomerVendor.objects.get_or_create(
            customerVendorName='Test Customer 2',
            defaults={'type': 1, 'createdBy': user}
        )
        
        # Create active visit plan
        sys.stdout.write("Creating visit plan...\n")
        sys.stdout.flush()
        VisitPlan.objects.filter(agentID=agent).update(isActive=False) # Deactivate others
        visit_plan = VisitPlan.objects.create(
            agentID=agent,
            dateFrom=date.today(),
            dateTo=date.today(),
            customers=[customer1.id], # Only customer 1 is assigned
            isActive=True,
            createdBy=user
        )
        
        # Create Account (Cash)
        sys.stdout.write("Creating account...\n")
        sys.stdout.flush()
        # Clean up test account if exists to avoid unique constraint issues
        Account.objects.filter(accountName='Test Cash Account').delete()
        
        account = Account.objects.create(
            accountName='Test Cash Account',
            sign=999999, # Random unique sign
            createdBy=user
        )

        # Create transactions
        sys.stdout.write("Creating transaction 1...\n")
        sys.stdout.flush()
        # Transaction 1: Customer 1 (Should be returned)
        t1 = Transaction.objects.create(
            accountID=account,
            amount=100.00,
            notes='Transaction for Customer 1',
            type=1,
            customerVendorID=customer1,
            createdBy=user
        )
        
        sys.stdout.write("Creating transaction 2...\n")
        sys.stdout.flush()
        # Transaction 2: Customer 2 (Should NOT be returned)
        t2 = Transaction.objects.create(
            accountID=account,
            amount=200.00,
            notes='Transaction for Customer 2',
            type=1,
            customerVendorID=customer2,
            createdBy=user
        )
        
        sys.stdout.write("Test data created.\n")
        sys.stdout.flush()
        
        # Test 1: Valid Credentials
        sys.stdout.write("\nTest 1: Valid Credentials\n")
        sys.stdout.flush()
        factory = RequestFactory()
        request = factory.get('/authentication/api/agents/customer_transactions/')
        
        # Add Basic Auth header
        credentials = f"{agent_username}:{agent_password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        request.META['HTTP_AUTHORIZATION'] = f'Basic {encoded_credentials}'
        
        response = customer_transactions_api(request)
        sys.stdout.write(f"Status Code: {response.status_code}\n")
        
        content = json.loads(response.content)
        sys.stdout.write(f"Response: {json.dumps(content, indent=2)}\n")
        sys.stdout.flush()
        
        if response.status_code == 200 and content['success']:
            transactions = content['transactions']
            if len(transactions) == 1 and transactions[0]['customer_name'] == 'Test Customer 1':
                sys.stdout.write("PASS: Correctly returned transaction for assigned customer only.\n")
            else:
                sys.stdout.write("FAIL: Incorrect transactions returned.\n")
        else:
            sys.stdout.write("FAIL: Request failed.\n")

        # Test 2: Invalid Credentials
        sys.stdout.write("\nTest 2: Invalid Credentials\n")
        sys.stdout.flush()
        request = factory.get('/authentication/api/agents/customer_transactions/')
        credentials = f"{agent_username}:wrongpassword"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        request.META['HTTP_AUTHORIZATION'] = f'Basic {encoded_credentials}'
        
        response = customer_transactions_api(request)
        sys.stdout.write(f"Status Code: {response.status_code}\n")
        
        if response.status_code == 401:
            sys.stdout.write("PASS: Correctly rejected invalid credentials.\n")
        else:
            sys.stdout.write(f"FAIL: Expected 401, got {response.status_code}\n")

        # Cleanup
        sys.stdout.write("\nCleaning up...\n")
        sys.stdout.flush()
        t1.delete()
        t2.delete()
        visit_plan.delete()
        agent.delete()
        account.delete()
        # Keep customers/store/user as they might be used by others or are generic
        
    except Exception as e:
        sys.stdout.write(f"ERROR: {str(e)}\n")
        sys.stdout.flush()
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_endpoint()
