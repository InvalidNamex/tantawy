# API Views for Invoice Management
# POST endpoint for creating all 4 types of invoices with transaction processing

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction as db_transaction
from django.db import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from .models import (
    InvoiceMaster, InvoiceDetail, Transaction, Account, 
    CustomerVendor, Item, Store
)
from .constants import *
import json

# Account IDs as specified in the documentation
CASH_ACCOUNT_ID = 35
VISA_ACCOUNT_ID = 10
VENDORS_DEFERRED_ACCOUNT_ID = 38
CUSTOMERS_DEFERRED_ACCOUNT_ID = 36

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
    
    # For return invoices, validate original invoice
    if invoice_type in [3, 4]:
        original_invoice_id = invoice_master_data.get('originalInvoiceID')
        if not original_invoice_id:
            return {'valid': False, 'message': 'Return invoices must reference an original invoice'}
        
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
    
    # Invoice Transaction: +netTotal (Debit)
    Transaction.objects.create(
        invoiceID=invoice_master,
        accountID=account,
        customerVendorID=invoice_master.customerOrVendorID,
        amount=invoice_master.netTotal,  # Positive for debit
        type=TRANSACTION_TYPE_PURCHASE,
        notes=f'Purchase Invoice #{invoice_master.id} - {invoice_master.notes}',
        createdBy=user,
        updatedBy=user
    )
    
    # Voucher Transaction (if not deferred): -netTotal (Credit)
    if invoice_master.paymentType != PAYMENT_TYPE_PARTIAL_DEFERRED:
        Transaction.objects.create(
            invoiceID=invoice_master,
            accountID=account,
            customerVendorID=invoice_master.customerOrVendorID,
            amount=-invoice_master.netTotal,  # Negative for credit
            type=2,  # Payment type
            notes=f'Payment for Purchase Invoice #{invoice_master.id}',
            createdBy=user,
            updatedBy=user
        )


def create_sales_transactions(invoice_master, account, user):
    """Create transactions for Sales Invoice (Type 2)"""
    
    # Invoice Transaction: -netTotal (Credit)
    Transaction.objects.create(
        invoiceID=invoice_master,
        accountID=account,
        customerVendorID=invoice_master.customerOrVendorID,
        amount=-invoice_master.netTotal,  # Negative for credit
        type=TRANSACTION_TYPE_SALES,
        notes=f'Sales Invoice #{invoice_master.id} - {invoice_master.notes}',
        createdBy=user,
        updatedBy=user
    )
    
    # Voucher Transaction (if not deferred): +netTotal (Debit)
    if invoice_master.paymentType != PAYMENT_TYPE_PARTIAL_DEFERRED:
        Transaction.objects.create(
            invoiceID=invoice_master,
            accountID=account,
            customerVendorID=invoice_master.customerOrVendorID,
            amount=invoice_master.netTotal,  # Positive for debit
            type=1,  # Receipt type
            notes=f'Receipt for Sales Invoice #{invoice_master.id}',
            createdBy=user,
            updatedBy=user
        )


def create_return_purchase_transactions(invoice_master, account, user):
    """Create transactions for Return Purchase Invoice (Type 3)"""
    
    # Invoice Transaction: -netTotal (Credit - opposite of purchase)
    Transaction.objects.create(
        invoiceID=invoice_master,
        accountID=account,
        customerVendorID=invoice_master.customerOrVendorID,
        amount=-invoice_master.netTotal,  # Negative for credit
        type=TRANSACTION_TYPE_RETURN_PURCHASE,
        notes=f'Return Purchase Invoice #{invoice_master.id} - {invoice_master.notes}',
        createdBy=user,
        updatedBy=user
    )
    
    # Voucher Transaction (if not deferred): +netTotal (Debit - opposite of purchase)
    if invoice_master.paymentType != PAYMENT_TYPE_PARTIAL_DEFERRED:
        Transaction.objects.create(
            invoiceID=invoice_master,
            accountID=account,
            customerVendorID=invoice_master.customerOrVendorID,
            amount=invoice_master.netTotal,  # Positive for debit
            type=1,  # Receipt type (we receive money back)
            notes=f'Receipt for Return Purchase Invoice #{invoice_master.id}',
            createdBy=user,
            updatedBy=user
        )


def create_return_sales_transactions(invoice_master, account, user):
    """Create transactions for Return Sales Invoice (Type 4)"""
    
    # Invoice Transaction: +netTotal (Debit - opposite of sales)
    Transaction.objects.create(
        invoiceID=invoice_master,
        accountID=account,
        customerVendorID=invoice_master.customerOrVendorID,
        amount=invoice_master.netTotal,  # Positive for debit
        type=TRANSACTION_TYPE_RETURN_SALES,
        notes=f'Return Sales Invoice #{invoice_master.id} - {invoice_master.notes}',
        createdBy=user,
        updatedBy=user
    )
    
    # Voucher Transaction (if not deferred): -netTotal (Credit - opposite of sales)
    if invoice_master.paymentType != PAYMENT_TYPE_PARTIAL_DEFERRED:
        Transaction.objects.create(
            invoiceID=invoice_master,
            accountID=account,
            customerVendorID=invoice_master.customerOrVendorID,
            amount=-invoice_master.netTotal,  # Negative for credit
            type=2,  # Payment type (we pay money back)
            notes=f'Payment for Return Sales Invoice #{invoice_master.id}',
            createdBy=user,
            updatedBy=user
        )


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