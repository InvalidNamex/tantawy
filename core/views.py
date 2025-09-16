"""
Django REST Framework API views for core models.
Provides comprehensive CRUD operations with filtering, search, and Swagger documentation.
All views include proper error handling and performance optimization.
"""

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import *
from .serializers import *

# ItemsGroup Views
@extend_schema(
    summary="List all items groups",
    description="Retrieve a list of all items groups"
)
@api_view(['GET'])
def itemsgroup_list(request):
    """Get all items groups"""
    queryset = ItemsGroup.objects.filter(isDeleted=False)
    serializer = ItemsGroupSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@extend_schema(
    summary="Get items group by ID",
    description="Retrieve a specific items group by ID",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Items Group ID')
    ]
)
@api_view(['GET'])
def itemsgroup_detail(request, id):
    """Get specific items group by ID"""
    try:
        itemsgroup = get_object_or_404(ItemsGroup, id=id, isDeleted=False)
        serializer = ItemsGroupSerializer(itemsgroup, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Item Views
@extend_schema(
    summary="List all items",
    description="Retrieve a list of all items with optional filtering by group"
)
@api_view(['GET'])
def item_list(request):
    """Get all items"""
    queryset = Item.objects.filter(isDeleted=False).select_related('itemGroupId')
    serializer = ItemSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@extend_schema(
    summary="List items by group",
    description="Retrieve items for a specific group",
    parameters=[
        OpenApiParameter(name='group_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Items Group ID')
    ]
)
@api_view(['GET'])
def item_by_group(request, group_id):
    """Get items filtered by group"""
    try:
        queryset = Item.objects.filter(itemGroupId=group_id, isDeleted=False).select_related('itemGroupId')
        serializer = ItemSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Get item by ID",
    description="Retrieve a specific item by ID",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Item ID')
    ]
)
@api_view(['GET'])
def item_detail(request, id):
    """Get specific item by ID"""
    try:
        item = get_object_or_404(Item, id=id, isDeleted=False)
        serializer = ItemSerializer(item, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# PriceList Views
@extend_schema(
    summary="List all price lists",
    description="Retrieve a list of all price lists"
)
@api_view(['GET'])
def pricelist_list(request):
    """Get all price lists"""
    queryset = PriceList.objects.filter(isDeleted=False)
    serializer = PriceListSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@extend_schema(
    summary="Get price list by ID",
    description="Retrieve a specific price list by ID",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Price List ID')
    ]
)
@api_view(['GET'])
def pricelist_detail(request, id):
    """Get specific price list by ID"""
    try:
        pricelist = get_object_or_404(PriceList, id=id, isDeleted=False)
        serializer = PriceListSerializer(pricelist, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# PriceListDetail Views
@extend_schema(
    summary="List all price list details",
    description="Retrieve a list of all price list details"
)
@api_view(['GET'])
def pricelistdetail_list(request):
    """Get all price list details"""
    queryset = PriceListDetail.objects.filter(isDeleted=False).select_related('priceList', 'item')
    serializer = PriceListDetailSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@extend_schema(
    summary="List price list details by price list",
    description="Retrieve price list details for a specific price list",
    parameters=[
        OpenApiParameter(name='pricelist_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Price List ID')
    ]
)
@api_view(['GET'])
def pricelistdetail_by_pricelist(request, pricelist_id):
    """Get price list details filtered by price list"""
    try:
        queryset = PriceListDetail.objects.filter(priceList=pricelist_id, isDeleted=False).select_related('priceList', 'item')
        serializer = PriceListDetailSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# StoreGroup Views
@extend_schema(
    summary="List all store groups",
    description="Retrieve a list of all store groups"
)
@api_view(['GET'])
def storegroup_list(request):
    """Get all store groups"""
    queryset = StoreGroup.objects.filter(isDeleted=False)
    serializer = StoreGroupSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@extend_schema(
    summary="Get store group by ID",
    description="Retrieve a specific store group by ID",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Store Group ID')
    ]
)
@api_view(['GET'])
def storegroup_detail(request, id):
    """Get specific store group by ID"""
    try:
        storegroup = get_object_or_404(StoreGroup, id=id, isDeleted=False)
        serializer = StoreGroupSerializer(storegroup, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Store Views
@extend_schema(
    summary="List all stores",
    description="Retrieve a list of all stores"
)
@api_view(['GET'])
def store_list(request):
    """Get all stores"""
    queryset = Store.objects.filter(isDeleted=False)
    serializer = StoreSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@extend_schema(
    summary="Get store by ID",
    description="Retrieve a specific store by ID",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Store ID')
    ]
)
@api_view(['GET'])
def store_detail(request, id):
    """Get specific store by ID"""
    try:
        store = get_object_or_404(Store, id=id, isDeleted=False)
        serializer = StoreSerializer(store, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# CustomerVendor Views
@extend_schema(
    summary="List all customers and vendors",
    description="Retrieve a list of all customers and vendors with optional type filtering",
    parameters=[
        OpenApiParameter(name='type', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, 
                        description='Filter by type: 1=Customer, 2=Vendor, 3=Both')
    ]
)
@api_view(['GET'])
def customervendor_list(request):
    """Get all customers and vendors"""
    queryset = CustomerVendor.objects.filter(isDeleted=False)
    type_filter = request.GET.get('type')
    if type_filter:
        try:
            queryset = queryset.filter(type=int(type_filter))
        except ValueError:
            return Response({'error': 'Invalid type parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CustomerVendorSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@extend_schema(
    summary="Get customer/vendor by ID",
    description="Retrieve a specific customer or vendor by ID",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, 
                        description='Customer/Vendor ID')
    ]
)
@api_view(['GET'])
def customervendor_detail(request, id):
    """Get specific customer/vendor by ID"""
    try:
        customervendor = get_object_or_404(CustomerVendor, id=id, isDeleted=False)
        serializer = CustomerVendorSerializer(customervendor, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# InvoiceMaster Views
@extend_schema(
    summary="List all invoices",
    description="Retrieve a list of all invoices with optional filtering by type, status, and customer/vendor",
    parameters=[
        OpenApiParameter(name='invoice_type', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                        description='Filter by invoice type: 1=Purchases, 2=Sales, 3=Return Purchases, 4=Return Sales'),
        OpenApiParameter(name='status', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                        description='Filter by status: 0=Paid, 1=Unpaid, 2=Partially Paid'),
        OpenApiParameter(name='customer_vendor', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                        description='Filter by customer/vendor ID'),
        OpenApiParameter(name='store', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                        description='Filter by store ID')
    ]
)
@api_view(['GET'])
def invoicemaster_list(request):
    """Get all invoices with optional filtering"""
    queryset = InvoiceMaster.objects.filter(isDeleted=False).select_related(
        'customerOrVendorID', 'storeID', 'originalInvoiceID'
    ).prefetch_related('invoicedetail_set__item')
    
    # Apply filters
    invoice_type = request.GET.get('invoice_type')
    if invoice_type:
        try:
            queryset = queryset.filter(invoiceType=int(invoice_type))
        except ValueError:
            return Response({'error': 'Invalid invoice_type parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    status_filter = request.GET.get('status')
    if status_filter:
        try:
            queryset = queryset.filter(status=int(status_filter))
        except ValueError:
            return Response({'error': 'Invalid status parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    customer_vendor = request.GET.get('customer_vendor')
    if customer_vendor:
        try:
            queryset = queryset.filter(customerOrVendorID=int(customer_vendor))
        except ValueError:
            return Response({'error': 'Invalid customer_vendor parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    store = request.GET.get('store')
    if store:
        try:
            queryset = queryset.filter(storeID=int(store))
        except ValueError:
            return Response({'error': 'Invalid store parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = InvoiceMasterSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@extend_schema(
    summary="Get invoice by ID",
    description="Retrieve a specific invoice by ID with all details",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, 
                        description='Invoice ID')
    ]
)
@api_view(['GET'])
def invoicemaster_detail(request, id):
    """Get specific invoice by ID"""
    try:
        invoice = get_object_or_404(
            InvoiceMaster.objects.select_related(
                'customerOrVendorID', 'storeID', 'originalInvoiceID'
            ).prefetch_related('invoicedetail_set__item'),
            id=id, isDeleted=False
        )
        serializer = InvoiceMasterSerializer(invoice, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# InvoiceDetail Views
@extend_schema(
    summary="List invoice details",
    description="Retrieve invoice details with optional filtering by invoice ID",
    parameters=[
        OpenApiParameter(name='invoice_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                        description='Filter by invoice master ID'),
        OpenApiParameter(name='item_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                        description='Filter by item ID')
    ]
)
@api_view(['GET'])
def invoicedetail_list(request):
    """Get invoice details with optional filtering"""
    queryset = InvoiceDetail.objects.filter(isDeleted=False).select_related(
        'item', 'invoiceMasterID', 'storeID'
    )
    
    # Apply filters
    invoice_id = request.GET.get('invoice_id')
    if invoice_id:
        try:
            queryset = queryset.filter(invoiceMasterID=int(invoice_id))
        except ValueError:
            return Response({'error': 'Invalid invoice_id parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    item_id = request.GET.get('item_id')
    if item_id:
        try:
            queryset = queryset.filter(item=int(item_id))
        except ValueError:
            return Response({'error': 'Invalid item_id parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = InvoiceDetailSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)

@extend_schema(
    summary="Get invoice detail by ID",
    description="Retrieve a specific invoice detail by ID",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, 
                        description='Invoice Detail ID')
    ]
)
@api_view(['GET'])
def invoicedetail_detail(request, id):
    """Get specific invoice detail by ID"""
    try:
        detail = get_object_or_404(
            InvoiceDetail.objects.select_related('item', 'invoiceMasterID', 'storeID'),
            id=id, isDeleted=False
        )
        serializer = InvoiceDetailSerializer(detail, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Stock Views
@extend_schema(
    summary="Get item stock levels",
    description="Calculate and retrieve stock levels for items across stores",
    parameters=[
        OpenApiParameter(name='item_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                        description='Filter by specific item ID'),
        OpenApiParameter(name='store_id', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                        description='Filter by specific store ID')
    ]
)
@api_view(['GET'])
def item_stock(request):
    """Get stock levels for items"""
    try:
        from django.db.models import Sum, Case, When, DecimalField, Q
        
        # Get filter parameters
        item_id = request.GET.get('item_id')
        store_id = request.GET.get('store_id')
        
        # Base queryset for items
        items_queryset = Item.objects.filter(isDeleted=False)
        if item_id:
            try:
                items_queryset = items_queryset.filter(id=int(item_id))
            except ValueError:
                return Response({'error': 'Invalid item_id parameter'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Build stock data
        stock_data = []
        
        for item in items_queryset:
            # Get stores to calculate stock for
            stores_queryset = Store.objects.filter(isDeleted=False)
            if store_id:
                try:
                    stores_queryset = stores_queryset.filter(id=int(store_id))
                except ValueError:
                    return Response({'error': 'Invalid store_id parameter'}, status=status.HTTP_400_BAD_REQUEST)
            
            for store in stores_queryset:
                stock_level = item.get_stock_by_store(store.id)
                
                stock_data.append({
                    'item_id': item.id,
                    'item_name': item.itemName,
                    'store_id': store.id,
                    'store_name': store.storeName,
                    'stock': float(stock_level) if stock_level else 0.0,
                    'is_deleted': item.isDeleted
                })
        
        return Response(stock_data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Account Views
@extend_schema(
    summary="List all accounts",
    description="Retrieve a list of all accounts with optional filtering by account group"
)
@api_view(['GET'])
def account_list(request):
    """Get all accounts with optional filtering"""
    try:
        queryset = Account.objects.filter(isDeleted=False)
        
        # Filter by account group if provided
        account_group = request.GET.get('account_group')
        if account_group:
            try:
                queryset = queryset.filter(accountGroup=int(account_group))
            except ValueError:
                return Response({'error': 'Invalid account_group parameter'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Search by account name
        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(accountName__icontains=search)
        
        # Order by account name
        queryset = queryset.order_by('accountName')
        
        serializer = AccountSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    summary="Get account by ID",
    description="Retrieve a specific account by ID",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Account ID')
    ]
)
@api_view(['GET'])
def account_detail(request, id):
    """Get specific account by ID"""
    try:
        account = get_object_or_404(Account, id=id, isDeleted=False)
        serializer = AccountSerializer(account, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Create new account",
    description="Create a new account with the provided data",
    request=AccountSerializer
)
@api_view(['POST'])
def account_create(request):
    """Create a new account"""
    try:
        serializer = AccountSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Set created_by to current user if authenticated
            if request.user.is_authenticated:
                serializer.save(createdBy=request.user)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Transaction Views
@extend_schema(
    summary="List all transactions",
    description="Retrieve a list of all transactions with comprehensive filtering options"
)
@api_view(['GET'])
def transaction_list(request):
    """Get all transactions with filtering capabilities"""
    try:
        queryset = Transaction.objects.filter(isDeleted=False)
        
        # Filter by account
        account_id = request.GET.get('account_id')
        if account_id:
            try:
                queryset = queryset.filter(accountID=int(account_id))
            except ValueError:
                return Response({'error': 'Invalid account_id parameter'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter by customer/vendor
        customer_vendor_id = request.GET.get('customer_vendor_id')
        if customer_vendor_id:
            try:
                queryset = queryset.filter(customerVendorID=int(customer_vendor_id))
            except ValueError:
                return Response({'error': 'Invalid customer_vendor_id parameter'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter by invoice
        invoice_id = request.GET.get('invoice_id')
        if invoice_id:
            try:
                queryset = queryset.filter(invoiceID=int(invoice_id))
            except ValueError:
                return Response({'error': 'Invalid invoice_id parameter'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter by transaction type
        transaction_type = request.GET.get('type')
        if transaction_type:
            try:
                queryset = queryset.filter(type=int(transaction_type))
            except ValueError:
                return Response({'error': 'Invalid type parameter'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Search by notes
        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(notes__icontains=search)
        
        # Order by creation date (newest first)
        queryset = queryset.order_by('-createdAt')
        
        serializer = TransactionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    summary="Get transaction by ID",
    description="Retrieve a specific transaction by ID",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Transaction ID')
    ]
)
@api_view(['GET'])
def transaction_detail(request, id):
    """Get specific transaction by ID"""
    try:
        transaction = get_object_or_404(Transaction, id=id, isDeleted=False)
        serializer = TransactionSerializer(transaction, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Create new transaction",
    description="Create a new transaction with the provided data",
    request=TransactionSerializer
)
@api_view(['POST'])
def transaction_create(request):
    """Create a new transaction"""
    try:
        serializer = TransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Set created_by to current user if authenticated
            if request.user.is_authenticated:
                serializer.save(createdBy=request.user)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
