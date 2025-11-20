# API Views for Invoice Management
# POST endpoint for creating all 4 types of invoices with transaction processing

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction as db_transaction
from django.db import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from functools import wraps
import base64
from .models import (
    InvoiceMaster, InvoiceDetail, Transaction, Account, 
    CustomerVendor, Item, Store, Agent
)
from .constants import *
import json

# Account IDs as specified in the documentation
CASH_ACCOUNT_ID = 35
VISA_ACCOUNT_ID = 10
VENDORS_DEFERRED_ACCOUNT_ID = 38
CUSTOMERS_DEFERRED_ACCOUNT_ID = 36


def agent_authentication_required(view_func):
    """
    Decorator for agent authentication using HTTP Basic Auth.
    Expects Authorization header with base64 encoded agentUsername:agentPassword
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Get Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Basic '):
            return Response({
                'success': False,
                'error': 'AUTHENTICATION_REQUIRED',
                'message': 'Agent authentication required. Use Basic Auth with agent credentials.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            # Decode credentials
            encoded_credentials = auth_header.split(' ')[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':')
            
            # Find and authenticate agent
            agent = Agent.objects.filter(
                agentUsername=username, 
                isDeleted=False,
                isActive=True
            ).first()
            
            if not agent or not agent.check_password(password):
                return Response({
                    'success': False,
                    'error': 'INVALID_CREDENTIALS',
                    'message': 'Invalid agent credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Add agent to request
            request.agent = agent
            return view_func(request, *args, **kwargs)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': 'AUTHENTICATION_ERROR',
                'message': f'Authentication failed: {str(e)}'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return _wrapped_view


@extend_schema(
    summary="Create Invoice",
    description="""Create invoice with all 4 types support:
    1. Purchase Invoice (Type: 1)
    2. Sales Invoice (Type: 2) 
    3. Return Purchase Invoice (Type: 3)
    4. Return Sales Invoice (Type: 4)
    
    Handles transaction creation based on invoice type and payment type.""",
    request={
        'application/json': {
            'example': {
                "invoiceMaster": {
                    "invoiceType": 2,
                    "customerOrVendorID": 15,
                    "storeId": 3,
                    "agentID": 1,
                    "status": 1,
                    "paymentType": 1,
                    "notes": "Sale to customer ABC Company",
                    "discountAmount": 50.00,
                    "discountPercentage": 5.0,
                    "taxAmount": 125.00,
                    "taxPercentage": 14.0,
                    "netTotal": 2375.00,
                    "totalPaid": 2375.00,
                    "returnStatus": 0,
                    "originalInvoiceID": None
                },
                "invoiceDetails": [
                    {
                        "item": 101,
                        "quantity": 5.0,
                        "price": 200.00,
                        "notes": "Premium product batch A"
                    },
                    {
                        "item": 205,
                        "quantity": 10.0,
                        "price": 150.00,
                        "notes": "Standard product batch B"
                    }
                ]
            }
        }
    },
    responses={
        201: {
            'description': 'Invoice created successfully',
            'example': {
                "success": True,
                "message": "Invoice created successfully",
                "data": {
                    "invoiceId": 1234,
                    "invoiceNumber": "INV-2025-001234",
                    "netTotal": 2375.00,
                    "status": "Created"
                }
            }
        },
        400: {
            'description': 'Validation error',
            'example': {
                "success": False,
                "message": "Validation failed",
                "errors": ["At least one item is required"]
            }
        }
    }
)
@api_view(['POST'])
@csrf_exempt
def create_invoice_api(request):
    """
    Create invoice with all 4 types support:
    1. Purchase Invoice (Type: 1)
    2. Sales Invoice (Type: 2) 
    3. Return Purchase Invoice (Type: 3)
    4. Return Sales Invoice (Type: 4)
    
    Handles transaction creation based on invoice type and payment type.
    """
    if not request.user.is_authenticated:
        return Response({
            'success': False,
            'message': 'Authentication required'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Parse request data
        invoice_master_data = request.data.get('invoiceMaster', {})
        invoice_details_data = request.data.get('invoiceDetails', [])
        
        # Validate required fields
        validation_result = validate_invoice_data(invoice_master_data, invoice_details_data)
        if not validation_result['valid']:
            return Response({
                'success': False,
                'message': validation_result['message']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Start database transaction
        with db_transaction.atomic():
            # Step 1: Create Invoice Master
            invoice_master = create_invoice_master(invoice_master_data, request.user)
            
            # Step 2: Create Invoice Details
            create_invoice_details(invoice_details_data, invoice_master, request.user)
            
            # Step 3: Create Accounting Transactions
            create_invoice_transactions(invoice_master, request.user)
            
            # Step 4: Update return status for original invoice (if return invoice)
            if invoice_master.originalInvoiceID:
                update_original_invoice_return_status(invoice_master.originalInvoiceID)
        
        return Response({
            'success': True,
            'invoiceId': invoice_master.id,
            'message': f'{get_invoice_type_name(invoice_master.invoiceType)} saved successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error creating invoice: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Batch Create Invoices",
    description="""Create multiple invoices in a single batch operation.
    All invoices will be processed in a single database transaction - if any invoice fails, 
    the entire batch will be rolled back to maintain data consistency.""",
    request={
        'application/json': {
            'example': {
                "invoices": [
                    {
                        "invoiceMaster": {
                            "invoiceType": 2,
                            "customerOrVendorID": 15,
                            "storeId": 3,
                            "agentID": 1,
                            "status": 1,
                            "paymentType": 1,
                            "notes": "Batch invoice #1",
                            "netTotal": 1000.00,
                            "totalPaid": 1000.00
                        },
                        "invoiceDetails": [
                            {
                                "item": 101,
                                "quantity": 2.0,
                                "price": 500.00,
                                "notes": "Item batch 1"
                            }
                        ]
                    },
                    {
                        "invoiceMaster": {
                            "invoiceType": 2,
                            "customerOrVendorID": 20,
                            "storeId": 3,
                            "agentID": 1,
                            "status": 1,
                            "paymentType": 1,
                            "notes": "Batch invoice #2",
                            "netTotal": 1500.00,
                            "totalPaid": 1500.00
                        },
                        "invoiceDetails": [
                            {
                                "item": 205,
                                "quantity": 3.0,
                                "price": 500.00,
                                "notes": "Item batch 2"
                            }
                        ]
                    }
                ]
            }
        }
    },
    responses={
        201: {
            'description': 'Batch invoices created successfully',
            'example': {
                "success": True,
                "message": "Batch processing completed successfully",
                "data": {
                    "totalInvoices": 2,
                    "createdInvoices": [
                        {
                            "invoiceId": 1234,
                            "invoiceType": "Sales",
                            "netTotal": 1000.00
                        },
                        {
                            "invoiceId": 1235,
                            "invoiceType": "Sales", 
                            "netTotal": 1500.00
                        }
                    ],
                    "totalAmount": 2500.00
                }
            }
        },
        400: {
            'description': 'Batch validation error',
            'example': {
                "success": False,
                "message": "Batch validation failed",
                "errors": [
                    "Invoice 1: At least one item is required",
                    "Invoice 2: Invalid customer ID"
                ]
            }
        }
    }
)
@api_view(['POST'])
@authentication_classes([])  # Disable DRF authentication
@permission_classes([AllowAny])  # Allow any user
@agent_authentication_required
def batch_create_invoices_api(request):
    """
    Create multiple invoices in a single batch operation.
    All invoices processed in atomic transaction for data consistency.
    Uses agent authentication from decorator - agent is available as request.agent
    """
    try:
        # Parse request data
        invoices_data = request.data.get('invoices', [])
        
        if not invoices_data:
            return Response({
                'success': False,
                'error': 'NO_INVOICES',
                'message': 'No invoices provided for batch processing'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(invoices_data) > 100:  # Limit batch size
            return Response({
                'success': False,
                'error': 'BATCH_SIZE_EXCEEDED',
                'message': 'Batch size limited to 100 invoices maximum'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate all invoices before processing
        validation_errors = []
        for idx, invoice_data in enumerate(invoices_data):
            invoice_master_data = invoice_data.get('invoiceMaster', {})
            invoice_details_data = invoice_data.get('invoiceDetails', [])
            
            validation_result = validate_invoice_data(invoice_master_data, invoice_details_data)
            if not validation_result['valid']:
                validation_errors.append(f"Invoice {idx + 1}: {validation_result['message']}")
        
        if validation_errors:
            return Response({
                'success': False,
                'error': 'VALIDATION_ERROR',
                'message': 'Batch validation failed',
                'errors': validation_errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use agent from decorator for audit fields
        audit_user = request.agent.createdBy if request.agent.createdBy else request.agent.updatedBy
        if not audit_user:
            # Fallback to first superuser if no valid user found
            from django.contrib.auth import get_user_model
            User = get_user_model()
            audit_user = User.objects.filter(is_superuser=True).first()
            
            if not audit_user:
                return Response({
                    'success': False,
                    'error': 'CONFIGURATION_ERROR',
                    'message': 'Unable to determine audit user'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Process all invoices in a single transaction
        created_invoices = []
        total_amount = Decimal('0')
        
        with db_transaction.atomic():
            for idx, invoice_data in enumerate(invoices_data):
                try:
                    invoice_master_data = invoice_data.get('invoiceMaster', {})
                    invoice_details_data = invoice_data.get('invoiceDetails', [])
                    
                    # Create Invoice Master
                    invoice_master = create_invoice_master(invoice_master_data, audit_user)
                    
                    # Create Invoice Details
                    create_invoice_details(invoice_details_data, invoice_master, audit_user)
                    
                    # Create Accounting Transactions
                    create_invoice_transactions(invoice_master, audit_user)
                    
                    # Update return status for original invoice (if return invoice)
                    if invoice_master.originalInvoiceID:
                        update_original_invoice_return_status(invoice_master.originalInvoiceID)
                    
                    # Add to results
                    created_invoices.append({
                        'invoiceId': invoice_master.id,
                        'invoiceType': get_invoice_type_name(invoice_master.invoiceType),
                        'netTotal': float(invoice_master.netTotal or 0),
                        'customerVendor': invoice_master.customerOrVendorID.customerVendorName if invoice_master.customerOrVendorID else None,
                        'agent': request.agent.agentName
                    })
                    
                    total_amount += invoice_master.netTotal or Decimal('0')
                    
                except Exception as e:
                    # This will cause the entire transaction to rollback
                    raise Exception(f"Error processing invoice {idx + 1}: {str(e)}")
        
        return Response({
            'success': True,
            'message': f'{len(created_invoices)} invoices created successfully',
            'data': {
                'totalInvoices': len(created_invoices),
                'createdInvoices': created_invoices,
                'totalAmount': float(total_amount)
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': 'PROCESSING_ERROR',
            'message': f'Batch processing failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def validate_invoice_data(invoice_master_data, invoice_details_data):
    """Validate invoice data before processing"""
    
    # Check required master fields
    required_fields = ['invoiceType', 'customerOrVendorID', 'storeId', 'paymentType', 'netTotal']
    for field in required_fields:
        if not invoice_master_data.get(field):
            return {'valid': False, 'message': f'Missing required field: {field}'}
    
    # Validate invoice type
    invoice_type = invoice_master_data.get('invoiceType')
    if invoice_type not in [1, 2, 3, 4]:
        return {'valid': False, 'message': 'Invalid invoice type. Must be 1, 2, 3, or 4'}
    
    # Validate payment type
    payment_type = invoice_master_data.get('paymentType')
    if payment_type not in [1, 2, 3]:
        return {'valid': False, 'message': 'Invalid payment type. Must be 1 (Cash), 2 (Visa), or 3 (Deferred)'}
    
    # Check if customer/vendor exists
    try:
        CustomerVendor.objects.get(id=invoice_master_data['customerOrVendorID'], isDeleted=False)
    except CustomerVendor.DoesNotExist:
        return {'valid': False, 'message': 'Customer/Vendor not found'}
    
    # Check if store exists
    try:
        Store.objects.get(id=invoice_master_data['storeId'], isDeleted=False)
    except Store.DoesNotExist:
        return {'valid': False, 'message': 'Store not found'}
    
    # Validate invoice details
    if not invoice_details_data:
        return {'valid': False, 'message': 'Invoice must have at least one line item'}
    
    for detail in invoice_details_data:
        if not detail.get('item') or not detail.get('quantity') or not detail.get('price'):
            return {'valid': False, 'message': 'Each line item must have item, quantity, and price'}
        
        # Check if item exists
        try:
            Item.objects.get(id=detail['item'], isDeleted=False)
        except Item.DoesNotExist:
            return {'valid': False, 'message': f'Item {detail["item"]} not found'}
    
    # For return invoices, optionally validate original invoice if provided
    if invoice_type in [3, 4]:
        original_invoice_id = invoice_master_data.get('originalInvoiceID')
        if original_invoice_id:
            try:
                original_invoice = InvoiceMaster.objects.get(id=original_invoice_id, isDeleted=False)
                # Validate return type matches original type
                if (invoice_type == 3 and original_invoice.invoiceType != 1) or \
                   (invoice_type == 4 and original_invoice.invoiceType != 2):
                    return {'valid': False, 'message': 'Return invoice type must match original invoice type'}
            except InvoiceMaster.DoesNotExist:
                return {'valid': False, 'message': 'Original invoice not found'}
    
    return {'valid': True, 'message': 'Validation passed'}


def create_invoice_master(invoice_data, user):
    """Create the invoice master record"""
    
    invoice_master = InvoiceMaster.objects.create(
        invoiceType=invoice_data['invoiceType'],
        customerOrVendorID_id=invoice_data['customerOrVendorID'],
        storeID_id=invoice_data['storeId'],
        agentID_id=invoice_data.get('agentID'),  # Added agentID field
        paymentType=invoice_data['paymentType'],
        notes=invoice_data.get('notes', ''),
        discountAmount=Decimal(str(invoice_data.get('discountAmount', 0))),
        discountPercentage=Decimal(str(invoice_data.get('discountPercentage', 0))),
        taxAmount=Decimal(str(invoice_data.get('taxAmount', 0))),
        taxPercentage=Decimal(str(invoice_data.get('taxPercentage', 0))),
        netTotal=Decimal(str(invoice_data['netTotal'])),
        status=invoice_data.get('status', STATUS_PAID),
        totalPaid=Decimal(str(invoice_data.get('totalPaid', 0))),
        returnStatus=invoice_data.get('returnStatus', RETURN_STATUS_NOT_RETURNED),
        originalInvoiceID_id=invoice_data.get('originalInvoiceID'),
        createdBy=user,
        updatedBy=user
    )
    
    return invoice_master


def create_invoice_details(details_data, invoice_master, user):
    """Create invoice detail records"""
    
    for detail in details_data:
        InvoiceDetail.objects.create(
            invoiceMasterID=invoice_master,
            item_id=detail['item'],
            quantity=Decimal(str(detail['quantity'])),
            price=Decimal(str(detail['price'])),
            notes=detail.get('notes', ''),
            storeID=invoice_master.storeID,
            discountAmount=Decimal(str(detail.get('discountAmount', 0))),
            discountPercentage=Decimal(str(detail.get('discountPercentage', 0))),
            taxAmount=Decimal(str(detail.get('taxAmount', 0))),
            taxPercentage=Decimal(str(detail.get('taxPercentage', 0))),
            createdBy=user,
            updatedBy=user
        )


def create_invoice_transactions(invoice_master, user):
    """Create accounting transactions based on invoice type and payment type"""
    
    invoice_type = invoice_master.invoiceType
    payment_type = invoice_master.paymentType
    net_total = invoice_master.netTotal
    
    # Determine account ID based on payment type
    if payment_type == PAYMENT_TYPE_CASH:
        account_id = CASH_ACCOUNT_ID
    elif payment_type == PAYMENT_TYPE_VISA:
        account_id = VISA_ACCOUNT_ID
    elif payment_type == PAYMENT_TYPE_PARTIAL_DEFERRED:
        if invoice_type in [INVOICE_TYPE_PURCHASES, INVOICE_TYPE_RETURN_PURCHASES]:
            account_id = VENDORS_DEFERRED_ACCOUNT_ID
        else:  # Sales or Return Sales
            account_id = CUSTOMERS_DEFERRED_ACCOUNT_ID
    
    # Get account object
    try:
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        raise Exception(f'Account with ID {account_id} not found')
    
    # Create transactions based on invoice type
    if invoice_type == INVOICE_TYPE_PURCHASES:
        create_purchase_transactions(invoice_master, account, user)
    elif invoice_type == INVOICE_TYPE_SALES:
        create_sales_transactions(invoice_master, account, user)
    elif invoice_type == INVOICE_TYPE_RETURN_PURCHASES:
        create_return_purchase_transactions(invoice_master, account, user)
    elif invoice_type == INVOICE_TYPE_RETURN_SALES:
        create_return_sales_transactions(invoice_master, account, user)


def create_purchase_transactions(invoice_master, account, user):
    """Create transactions for Purchase Invoice (Type 1)"""
    
    # Always create the deferred/liability transaction
    Transaction.objects.create(
        invoiceID=invoice_master,
        accountID_id=38,  # Vendors Deferred Account
        customerVendorID=invoice_master.customerOrVendorID,
        amount=invoice_master.netTotal,  # Positive for debit (we owe vendor)
        type=TRANSACTION_TYPE_PURCHASE,
        notes=f'Purchase Invoice #{invoice_master.id} - {invoice_master.notes}',
        agentID=invoice_master.agentID,  # Set the agent who created this transaction
        createdBy=user,
        updatedBy=user
    )
    
    # Create payment transaction based on status
    if invoice_master.status == 0:  # Paid
        Transaction.objects.create(
            invoiceID=invoice_master,
            accountID=account,  # Cash/Visa account
            customerVendorID=invoice_master.customerOrVendorID,
            amount=-invoice_master.netTotal,  # Negative for credit (cash goes out)
            type=2,  # Payment type
            notes=f'Payment for Purchase Invoice #{invoice_master.id}',
            agentID=invoice_master.agentID,  # Set the agent who created this transaction
            createdBy=user,
            updatedBy=user
        )
    elif invoice_master.status == 2:  # Partially Paid
        Transaction.objects.create(
            invoiceID=invoice_master,
            accountID=account,  # Cash/Visa account
            customerVendorID=invoice_master.customerOrVendorID,
            amount=-invoice_master.totalPaid,  # Negative for credit (partial cash goes out)
            type=2,  # Payment type
            notes=f'Partial Payment for Purchase Invoice #{invoice_master.id}',
            agentID=invoice_master.agentID,  # Set the agent who created this transaction
            createdBy=user,
            updatedBy=user
        )
    # If status == 1 (Unpaid), no payment transaction is created


def create_sales_transactions(invoice_master, account, user):
    """Create transactions for Sales Invoice (Type 2)"""
    
    # Always create the deferred/receivable transaction
    Transaction.objects.create(
        invoiceID=invoice_master,
        accountID_id=36,  # Customers Deferred Account
        customerVendorID=invoice_master.customerOrVendorID,
        amount=-invoice_master.netTotal,  # Negative for credit (customer owes us)
        type=TRANSACTION_TYPE_SALES,
        notes=f'Sales Invoice #{invoice_master.id} - {invoice_master.notes}',
        agentID=invoice_master.agentID,  # Set the agent who created this transaction
        createdBy=user,
        updatedBy=user
    )
    
    # Create receipt transaction based on status
    if invoice_master.status == 0:  # Paid
        Transaction.objects.create(
            invoiceID=invoice_master,
            accountID=account,  # Cash/Visa account
            customerVendorID=invoice_master.customerOrVendorID,
            amount=invoice_master.netTotal,  # Positive for debit (cash comes in)
            type=1,  # Receipt type
            notes=f'Receipt for Sales Invoice #{invoice_master.id}',
            agentID=invoice_master.agentID,  # Set the agent who created this transaction
            createdBy=user,
            updatedBy=user
        )
    elif invoice_master.status == 2:  # Partially Paid
        Transaction.objects.create(
            invoiceID=invoice_master,
            accountID=account,  # Cash/Visa account
            customerVendorID=invoice_master.customerOrVendorID,
            amount=invoice_master.totalPaid,  # Positive for debit (partial cash comes in)
            type=1,  # Receipt type
            notes=f'Partial Receipt for Sales Invoice #{invoice_master.id}',
            agentID=invoice_master.agentID,  # Set the agent who created this transaction
            createdBy=user,
            updatedBy=user
        )
    # If status == 1 (Unpaid), no receipt transaction is created


def create_return_purchase_transactions(invoice_master, account, user):
    """Create transactions for Return Purchase Invoice (Type 3)"""
    
    # Always create the deferred/liability reversal transaction
    Transaction.objects.create(
        invoiceID=invoice_master,
        accountID_id=38,  # Vendors Deferred Account
        customerVendorID=invoice_master.customerOrVendorID,
        amount=-invoice_master.netTotal,  # Negative for credit (we owe vendor less)
        type=TRANSACTION_TYPE_RETURN_PURCHASE,
        notes=f'Return Purchase Invoice #{invoice_master.id} - {invoice_master.notes}',
        agentID=invoice_master.agentID,  # Set the agent who created this transaction
        createdBy=user,
        updatedBy=user
    )
    
    # Create receipt transaction based on status (if vendor refunds us)
    if invoice_master.status == 0:  # Paid (refunded)
        Transaction.objects.create(
            invoiceID=invoice_master,
            accountID=account,  # Cash/Visa account
            customerVendorID=invoice_master.customerOrVendorID,
            amount=invoice_master.netTotal,  # Positive for debit (cash comes in)
            type=1,  # Receipt type (we receive money back)
            notes=f'Receipt for Return Purchase Invoice #{invoice_master.id}',
            agentID=invoice_master.agentID,  # Set the agent who created this transaction
            createdBy=user,
            updatedBy=user
        )
    elif invoice_master.status == 2:  # Partially Paid (partially refunded)
        Transaction.objects.create(
            invoiceID=invoice_master,
            accountID=account,  # Cash/Visa account
            customerVendorID=invoice_master.customerOrVendorID,
            amount=invoice_master.totalPaid,  # Positive for debit (partial cash comes in)
            type=1,  # Receipt type
            notes=f'Partial Receipt for Return Purchase Invoice #{invoice_master.id}',
            agentID=invoice_master.agentID,  # Set the agent who created this transaction
            createdBy=user,
            updatedBy=user
        )
    # If status == 1 (Unpaid/Not Refunded), no receipt transaction is created


def create_return_sales_transactions(invoice_master, account, user):
    """Create transactions for Return Sales Invoice (Type 4)"""
    
    # Always create the deferred/receivable reversal transaction
    Transaction.objects.create(
        invoiceID=invoice_master,
        accountID_id=36,  # Customers Deferred Account
        customerVendorID=invoice_master.customerOrVendorID,
        amount=invoice_master.netTotal,  # Positive for debit (customer owes us less)
        type=TRANSACTION_TYPE_RETURN_SALES,
        notes=f'Return Sales Invoice #{invoice_master.id} - {invoice_master.notes}',
        agentID=invoice_master.agentID,  # Set the agent who created this transaction
        createdBy=user,
        updatedBy=user
    )
    
    # Create payment transaction based on status (if we refund customer)
    if invoice_master.status == 0:  # Paid (refunded)
        Transaction.objects.create(
            invoiceID=invoice_master,
            accountID=account,  # Cash/Visa account
            customerVendorID=invoice_master.customerOrVendorID,
            amount=-invoice_master.netTotal,  # Negative for credit (cash goes out)
            type=2,  # Payment type (we pay money back)
            notes=f'Payment for Return Sales Invoice #{invoice_master.id}',
            agentID=invoice_master.agentID,  # Set the agent who created this transaction
            createdBy=user,
            updatedBy=user
        )
    elif invoice_master.status == 2:  # Partially Paid (partially refunded)
        Transaction.objects.create(
            invoiceID=invoice_master,
            accountID=account,  # Cash/Visa account
            customerVendorID=invoice_master.customerOrVendorID,
            amount=-invoice_master.totalPaid,  # Negative for credit (partial cash goes out)
            type=2,  # Payment type
            notes=f'Partial Payment for Return Sales Invoice #{invoice_master.id}',
            agentID=invoice_master.agentID,  # Set the agent who created this transaction
            createdBy=user,
            updatedBy=user
        )
    # If status == 1 (Unpaid/Not Refunded), no payment transaction is created


def update_original_invoice_return_status(original_invoice):
    """Update the return status of the original invoice"""
    
    # Get all return invoices for this original invoice
    return_invoices = InvoiceMaster.objects.filter(
        originalInvoiceID=original_invoice,
        isDeleted=False
    )
    
    if not return_invoices.exists():
        return
    
    # Get original invoice details
    original_details = InvoiceDetail.objects.filter(
        invoiceMasterID=original_invoice,
        isDeleted=False
    )
    
    # Calculate return status based on quantities
    all_items_fully_returned = True
    any_items_returned = False
    
    for original_detail in original_details:
        # Calculate total returned quantity for this item
        total_returned = 0
        for return_invoice in return_invoices:
            return_detail = InvoiceDetail.objects.filter(
                invoiceMasterID=return_invoice,
                item=original_detail.item,
                isDeleted=False
            ).first()
            if return_detail:
                total_returned += return_detail.quantity
        
        if total_returned > 0:
            any_items_returned = True
        
        if total_returned < original_detail.quantity:
            all_items_fully_returned = False
    
    # Update return status
    if all_items_fully_returned and any_items_returned:
        original_invoice.returnStatus = RETURN_STATUS_FULLY_RETURNED
    elif any_items_returned:
        original_invoice.returnStatus = RETURN_STATUS_PARTIALLY_RETURNED
    else:
        original_invoice.returnStatus = RETURN_STATUS_NOT_RETURNED
    
    original_invoice.save()


def get_invoice_type_name(invoice_type):
    """Get human readable invoice type name"""
    type_names = {
        1: 'Purchase Invoice',
        2: 'Sales Invoice',
        3: 'Return Purchase Invoice',
        4: 'Return Sales Invoice'
    }
    return type_names.get(invoice_type, 'Unknown Invoice Type')


@extend_schema(
    summary="Get Available Returns",
    description="Get available items for return from an original invoice. Returns items with available quantities that can still be returned",
    parameters=[
        OpenApiParameter(name='invoice_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Original Invoice ID')
    ],
    responses={
        200: {
            'description': 'Available return items retrieved successfully',
            'example': {
                "success": True,
                "data": {
                    "originalInvoice": {
                        "id": 123,
                        "invoiceType": 2,
                        "netTotal": 1500.00,
                        "returnStatus": 1
                    },
                    "availableItems": [
                        {
                            "itemId": 101,
                            "itemName": "Product A",
                            "originalQuantity": 10.0,
                            "returnedQuantity": 2.0,
                            "availableQuantity": 8.0,
                            "price": 150.00
                        }
                    ]
                }
            }
        }
    }
)
@api_view(['GET'])
def get_available_returns_api(request, invoice_id):
    """
    Get available items for return from an original invoice
    Returns items with available quantities that can still be returned
    """
    try:
        original_invoice = InvoiceMaster.objects.get(id=invoice_id, isDeleted=False)
        
        # Get original invoice details
        original_details = InvoiceDetail.objects.filter(
            invoiceMasterID=original_invoice,
            isDeleted=False
        )
        
        # Get all return invoices for this original invoice
        return_invoices = InvoiceMaster.objects.filter(
            originalInvoiceID=original_invoice,
            isDeleted=False
        )
        
        available_items = []
        
        for original_detail in original_details:
            # Calculate total returned quantity for this item
            total_returned = 0
            for return_invoice in return_invoices:
                return_detail = InvoiceDetail.objects.filter(
                    invoiceMasterID=return_invoice,
                    item=original_detail.item,
                    isDeleted=False
                ).first()
                if return_detail:
                    total_returned += return_detail.quantity
            
            available_for_return = original_detail.quantity - total_returned
            
            if available_for_return > 0:
                available_items.append({
                    'itemId': original_detail.item.id,
                    'itemName': original_detail.item.itemName,
                    'originalQuantity': float(original_detail.quantity),
                    'totalReturned': float(total_returned),
                    'availableForReturn': float(available_for_return),
                    'price': float(original_detail.price)
                })
        
        return Response({
            'success': True,
            'invoiceId': invoice_id,
            'items': available_items
        }, status=status.HTTP_200_OK)
        
    except InvoiceMaster.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Invoice not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error retrieving available returns: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Get Invoices by Type",
    description="Get invoices filtered by type with sorting and filtering options. Types: 1=Purchase, 2=Sales, 3=Return Purchase, 4=Return Sales",
    parameters=[
        OpenApiParameter(name='invoice_type', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, 
                        description='Invoice Type (1=Purchase, 2=Sales, 3=Return Purchase, 4=Return Sales)'),
        OpenApiParameter(name='customer_vendor_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, 
                        description='Filter by customer/vendor ID'),
        OpenApiParameter(name='store_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, 
                        description='Filter by store ID'),
        OpenApiParameter(name='status', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, 
                        description='Filter by invoice status'),
        OpenApiParameter(name='from_date', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY, 
                        description='Filter from date (YYYY-MM-DD)'),
        OpenApiParameter(name='to_date', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY, 
                        description='Filter to date (YYYY-MM-DD)'),
        OpenApiParameter(name='sort_by', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, 
                        description='Sort field (default: createdOn)'),
        OpenApiParameter(name='sort_order', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, 
                        description='Sort order (asc/desc, default: desc)')
    ],
    responses={
        200: {
            'description': 'Invoices retrieved successfully',
            'example': {
                "success": True,
                "data": [
                    {
                        "id": 123,
                        "invoiceType": 2,
                        "customerOrVendorName": "ABC Company",
                        "storeName": "Main Store",
                        "netTotal": 1500.00,
                        "status": 1,
                        "createdOn": "2025-09-18T15:30:00Z"
                    }
                ]
            }
        }
    }
)
@api_view(['GET'])
def get_invoices_by_type_api(request, invoice_type):
    """
    Get invoices filtered by type with sorting and filtering options
    Types: 1=Purchase, 2=Sales, 3=Return Purchase, 4=Return Sales
    """
    try:
        # Validate invoice type
        if invoice_type not in [1, 2, 3, 4]:
            return Response({
                'success': False,
                'message': 'Invalid invoice type. Must be 1, 2, 3, or 4'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get query parameters
        search = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', 'createdAt')
        sort_order = request.GET.get('sort_order', 'desc')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        
        # Build queryset
        queryset = InvoiceMaster.objects.filter(
            invoiceType=invoice_type,
            isDeleted=False
        ).select_related('customerOrVendorID', 'storeID', 'createdBy')
        
        # Apply search filter
        if search:
            queryset = queryset.filter(
                models.Q(customerOrVendorID__customerVendorName__icontains=search) |
                models.Q(notes__icontains=search) |
                models.Q(id__icontains=search)
            )
        
        # Apply sorting
        if sort_order == 'desc':
            sort_by = f'-{sort_by}'
        
        queryset = queryset.order_by(sort_by)
        
        # Apply pagination
        start = (page - 1) * page_size
        end = start + page_size
        invoices = queryset[start:end]
        total_count = queryset.count()
        
        # Serialize data
        invoice_data = []
        for invoice in invoices:
            invoice_data.append({
                'id': invoice.id,
                'customerOrVendorName': invoice.customerOrVendorID.customerVendorName if invoice.customerOrVendorID else '',
                'storeName': invoice.storeID.storeName if invoice.storeID else '',
                'netTotal': float(invoice.netTotal) if invoice.netTotal else 0,
                'paymentType': invoice.get_paymentType_display(),
                'status': invoice.get_status_display(),
                'returnStatus': invoice.get_returnStatus_display(),
                'notes': invoice.notes or '',
                'createdBy': invoice.createdBy.username if invoice.createdBy else '',
                'createdAt': invoice.createdAt.isoformat() if invoice.createdAt else '',
                'updatedAt': invoice.updatedAt.isoformat() if invoice.updatedAt else ''
            })
        
        return Response({
            'success': True,
            'invoices': invoice_data,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': (total_count + page_size - 1) // page_size
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error retrieving invoices: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Get Invoice Detail",
    description="Get detailed information about a specific invoice including line items",
    parameters=[
        OpenApiParameter(name='invoice_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Invoice ID')
    ],
    responses={
        200: {
            'description': 'Invoice details retrieved successfully',
            'example': {
                "success": True,
                "data": {
                    "invoice": {
                        "id": 123,
                        "invoiceType": 2,
                        "customerOrVendorName": "ABC Company",
                        "storeName": "Main Store",
                        "netTotal": 1500.00,
                        "totalPaid": 1500.00,
                        "status": 1,
                        "paymentType": 1,
                        "notes": "Sale to customer",
                        "createdOn": "2025-09-18T15:30:00Z"
                    },
                    "invoiceDetails": [
                        {
                            "id": 456,
                            "itemName": "Product A",
                            "quantity": 10.0,
                            "price": 150.00,
                            "notes": "Premium product"
                        }
                    ]
                }
            }
        },
        404: {
            'description': 'Invoice not found',
            'example': {
                "success": False,
                "message": "Invoice not found"
            }
        }
    }
)
@api_view(['GET'])
def get_invoice_detail_api(request, invoice_id):
    """
    Get detailed information about a specific invoice including line items
    """
    try:
        invoice = InvoiceMaster.objects.select_related(
            'customerOrVendorID', 'storeID', 'createdBy', 'originalInvoiceID'
        ).get(id=invoice_id, isDeleted=False)
        
        # Get invoice details
        invoice_details = InvoiceDetail.objects.filter(
            invoiceMasterID=invoice,
            isDeleted=False
        ).select_related('item')
        
        # Get transactions
        transactions = Transaction.objects.filter(
            invoiceID=invoice,
            isDeleted=False
        ).select_related('accountID')
        
        # Serialize invoice master
        invoice_data = {
            'id': invoice.id,
            'invoiceType': invoice.invoiceType,
            'invoiceTypeName': invoice.get_invoiceType_display(),
            'customerOrVendorID': invoice.customerOrVendorID.id if invoice.customerOrVendorID else None,
            'customerOrVendorName': invoice.customerOrVendorID.customerVendorName if invoice.customerOrVendorID else '',
            'storeID': invoice.storeID.id if invoice.storeID else None,
            'storeName': invoice.storeID.storeName if invoice.storeID else '',
            'paymentType': invoice.paymentType,
            'paymentTypeName': invoice.get_paymentType_display(),
            'status': invoice.status,
            'statusName': invoice.get_status_display(),
            'returnStatus': invoice.returnStatus,
            'returnStatusName': invoice.get_returnStatus_display(),
            'notes': invoice.notes or '',
            'discountAmount': float(invoice.discountAmount) if invoice.discountAmount else 0,
            'discountPercentage': float(invoice.discountPercentage) if invoice.discountPercentage else 0,
            'taxAmount': float(invoice.taxAmount) if invoice.taxAmount else 0,
            'taxPercentage': float(invoice.taxPercentage) if invoice.taxPercentage else 0,
            'netTotal': float(invoice.netTotal) if invoice.netTotal else 0,
            'totalPaid': float(invoice.totalPaid) if invoice.totalPaid else 0,
            'originalInvoiceID': invoice.originalInvoiceID.id if invoice.originalInvoiceID else None,
            'createdBy': invoice.createdBy.username if invoice.createdBy else '',
            'createdAt': invoice.createdAt.isoformat() if invoice.createdAt else '',
            'updatedAt': invoice.updatedAt.isoformat() if invoice.updatedAt else ''
        }
        
        # Serialize invoice details
        details_data = []
        for detail in invoice_details:
            details_data.append({
                'id': detail.id,
                'itemID': detail.item.id,
                'itemName': detail.item.itemName,
                'quantity': float(detail.quantity) if detail.quantity else 0,
                'price': float(detail.price) if detail.price else 0,
                'notes': detail.notes or '',
                'discountAmount': float(detail.discountAmount) if detail.discountAmount else 0,
                'discountPercentage': float(detail.discountPercentage) if detail.discountPercentage else 0,
                'taxAmount': float(detail.taxAmount) if detail.taxAmount else 0,
                'taxPercentage': float(detail.taxPercentage) if detail.taxPercentage else 0,
                'lineTotal': float((detail.quantity or 0) * (detail.price or 0) - (detail.discountAmount or 0) + (detail.taxAmount or 0))
            })
        
        # Serialize transactions
        transactions_data = []
        for transaction in transactions:
            transactions_data.append({
                'id': transaction.id,
                'accountID': transaction.accountID.id,
                'accountName': transaction.accountID.accountName,
                'amount': float(transaction.amount) if transaction.amount else 0,
                'type': transaction.type,
                'notes': transaction.notes or '',
                'createdAt': transaction.createdAt.isoformat() if transaction.createdAt else ''
            })
        
        return Response({
            'success': True,
            'invoice': invoice_data,
            'details': details_data,
            'transactions': transactions_data
        }, status=status.HTTP_200_OK)
        
    except InvoiceMaster.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Invoice not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error retrieving invoice details: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Get Agent Invoices",
    description="""Get invoices for the authenticated agent with detailed information.
    Returns discount amount, tax amount, total paid, payment type, and invoice details (itemID, itemName, itemQuantity).
    Requires agent authentication using HTTP Basic Auth.""",
    parameters=[
        OpenApiParameter(name='from_date', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY, 
                        description='Filter from date (YYYY-MM-DD)'),
        OpenApiParameter(name='to_date', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY, 
                        description='Filter to date (YYYY-MM-DD)'),
        OpenApiParameter(name='invoice_type', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, 
                        description='Filter by invoice type (1=Purchase, 2=Sales, 3=Return Purchase, 4=Return Sales)'),
        OpenApiParameter(name='customer_vendor_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, 
                        description='Filter by customer/vendor ID'),
        OpenApiParameter(name='page', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, 
                        description='Page number (default: 1)'),
        OpenApiParameter(name='page_size', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, 
                        description='Items per page (default: 20, max: 100)')
    ],
    responses={
        200: {
            'description': 'Agent invoices retrieved successfully',
            'example': {
                "success": True,
                "data": {
                    "invoices": [
                        {
                            "invoiceId": 123,
                            "invoiceType": 2,
                            "invoiceTypeName": "Sales",
                            "customerOrVendorName": "ABC Company",
                            "discountAmount": 50.00,
                            "taxAmount": 125.00,
                            "netTotal": 1500.00,
                            "totalPaid": 1500.00,
                            "paymentType": 1,
                            "paymentTypeName": "Cash",
                            "createdAt": "2025-11-19T15:30:00Z",
                            "invoiceDetails": [
                                {
                                    "itemID": 101,
                                    "itemName": "Product A",
                                    "itemQuantity": 10.0
                                }
                            ]
                        }
                    ],
                    "pagination": {
                        "page": 1,
                        "pageSize": 20,
                        "totalCount": 45,
                        "totalPages": 3
                    }
                }
            }
        },
        401: {
            'description': 'Authentication required',
            'example': {
                "success": False,
                "error": "AUTHENTICATION_REQUIRED",
                "message": "Agent authentication required. Use Basic Auth with agent credentials."
            }
        }
    }
)
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
@agent_authentication_required
def get_agent_invoices_api(request):
    """
    Get invoices for the authenticated agent with detailed information.
    Returns discount amount, tax amount, total paid, payment type, and invoice details.
    Uses agent authentication from decorator - agent is available as request.agent
    """
    try:
        # Get query parameters
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        invoice_type = request.GET.get('invoice_type')
        customer_vendor_id = request.GET.get('customer_vendor_id')
        page = int(request.GET.get('page', 1))
        page_size = min(int(request.GET.get('page_size', 20)), 100)  # Max 100 per page
        
        # Build queryset for authenticated agent's invoices
        queryset = InvoiceMaster.objects.filter(
            agentID=request.agent,
            isDeleted=False
        ).select_related('customerOrVendorID', 'storeID', 'agentID')
        
        # Apply filters
        if from_date:
            queryset = queryset.filter(createdAt__gte=from_date)
        
        if to_date:
            queryset = queryset.filter(createdAt__lte=to_date)
        
        if invoice_type:
            queryset = queryset.filter(invoiceType=invoice_type)
        
        if customer_vendor_id:
            queryset = queryset.filter(customerOrVendorID_id=customer_vendor_id)
        
        # Order by newest first
        queryset = queryset.order_by('-createdAt')
        
        # Get total count
        total_count = queryset.count()
        
        # Apply pagination
        start = (page - 1) * page_size
        end = start + page_size
        invoices = queryset[start:end]
        
        # Serialize invoice data with details
        invoices_data = []
        for invoice in invoices:
            # Get invoice details
            invoice_details = InvoiceDetail.objects.filter(
                invoiceMasterID=invoice,
                isDeleted=False
            ).select_related('item')
            
            # Serialize details
            details_data = []
            for detail in invoice_details:
                details_data.append({
                    'itemID': detail.item.id,
                    'itemName': detail.item.itemName,
                    'itemQuantity': float(detail.quantity) if detail.quantity else 0
                })
            
            # Serialize invoice
            invoices_data.append({
                'invoiceId': invoice.id,
                'invoiceType': invoice.invoiceType,
                'invoiceTypeName': invoice.get_invoiceType_display(),
                'customerOrVendorName': invoice.customerOrVendorID.customerVendorName if invoice.customerOrVendorID else '',
                'customerOrVendorID': invoice.customerOrVendorID.id if invoice.customerOrVendorID else None,
                'discountAmount': float(invoice.discountAmount) if invoice.discountAmount else 0,
                'taxAmount': float(invoice.taxAmount) if invoice.taxAmount else 0,
                'netTotal': float(invoice.netTotal) if invoice.netTotal else 0,
                'totalPaid': float(invoice.totalPaid) if invoice.totalPaid else 0,
                'paymentType': invoice.paymentType,
                'paymentTypeName': invoice.get_paymentType_display(),
                'status': invoice.status,
                'statusName': invoice.get_status_display(),
                'createdAt': invoice.createdAt.isoformat() if invoice.createdAt else '',
                'invoiceDetails': details_data
            })
        
        return Response({
            'success': True,
            'data': {
                'invoices': invoices_data,
                'pagination': {
                    'page': page,
                    'pageSize': page_size,
                    'totalCount': total_count,
                    'totalPages': (total_count + page_size - 1) // page_size
                }
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': 'PROCESSING_ERROR',
            'message': f'Error retrieving agent invoices: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)