import os
import django
import json
import unittest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
from django.http import JsonResponse

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tantawy.settings')
django.setup()

from authentication.views import customer_transactions_api

class TestCustomerTransactions(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = '/authentication/api/agents/customer_transactions/'

    @patch('authentication.views.get_agent_basic_auth')
    @patch('core.models.VisitPlan.objects.filter')
    @patch('core.models.Transaction.objects.filter')
    def test_customer_transactions_success(self, mock_trans_filter, mock_vp_filter, mock_auth):
        # Mock Authentication
        mock_agent = MagicMock()
        mock_agent.id = 1
        mock_agent.agentName = 'Test Agent'
        mock_auth.return_value = (mock_agent, None)

        # Mock VisitPlan
        mock_vp = MagicMock()
        mock_vp.customers = [101, 102]
        mock_vp_queryset = MagicMock()
        mock_vp_queryset.first.return_value = mock_vp
        mock_vp_filter.return_value = mock_vp_queryset

        # Mock Transactions
        mock_t1 = MagicMock()
        mock_t1.createdAt.isoformat.return_value = '2023-01-01T10:00:00'
        mock_t1.amount = 100.00
        mock_t1.notes = 'Note 1'
        mock_t1.type = 1
        mock_t1.customerVendorID.customerVendorName = 'Customer 1'
        mock_t1.invoiceID.id = 501
        
        mock_t2 = MagicMock()
        mock_t2.createdAt.isoformat.return_value = '2023-01-02T11:00:00'
        mock_t2.amount = 200.00
        mock_t2.notes = 'Note 2'
        mock_t2.type = 2
        mock_t2.customerVendorID.customerVendorName = 'Customer 2'
        mock_t2.invoiceID = None # No invoice

        mock_trans_queryset = MagicMock()
        mock_trans_queryset.select_related.return_value.order_by.return_value = [mock_t1, mock_t2]
        mock_trans_filter.return_value = mock_trans_queryset

        # Make Request
        request = self.factory.get(self.url)
        response = customer_transactions_api(request)

        # Verify Response
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertTrue(content['success'])
        self.assertEqual(len(content['transactions']), 2)
        
        t1_data = content['transactions'][0]
        self.assertEqual(t1_data['customer_name'], 'Customer 1')
        self.assertEqual(t1_data['amount'], 100.0)
        self.assertEqual(t1_data['invoiceID'], 501)
        
        t2_data = content['transactions'][1]
        self.assertEqual(t2_data['customer_name'], 'Customer 2')
        self.assertEqual(t2_data['invoiceID'], None)
        
        print("PASS: test_customer_transactions_success")

    @patch('authentication.views.get_agent_basic_auth')
    def test_customer_transactions_auth_fail(self, mock_auth):
        # Mock Auth Failure
        error_response = JsonResponse({'success': False, 'message': 'Auth Failed'}, status=401)
        mock_auth.return_value = (None, error_response)

        request = self.factory.get(self.url)
        response = customer_transactions_api(request)

        self.assertEqual(response.status_code, 401)
        content = json.loads(response.content)
        self.assertFalse(content['success'])
        self.assertEqual(content['message'], 'Auth Failed')
        
        print("PASS: test_customer_transactions_auth_fail")

    @patch('authentication.views.get_agent_basic_auth')
    @patch('core.models.VisitPlan.objects.filter')
    def test_customer_transactions_no_plan(self, mock_vp_filter, mock_auth):
        # Mock Authentication
        mock_agent = MagicMock()
        mock_auth.return_value = (mock_agent, None)

        # Mock No Visit Plan
        mock_vp_queryset = MagicMock()
        mock_vp_queryset.first.return_value = None
        mock_vp_filter.return_value = mock_vp_queryset

        request = self.factory.get(self.url)
        response = customer_transactions_api(request)

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertTrue(content['success'])
        self.assertEqual(content['message'], 'No active visit plan found.')
        self.assertEqual(content['transactions'], [])
        
        print("PASS: test_customer_transactions_no_plan")

if __name__ == '__main__':
    unittest.main()
