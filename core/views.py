"""
Django REST Framework API views for core models.
Provides comprehensive CRUD operations with filtering, search, and Swagger documentation.
All views include proper error handling and performance optimization.
"""

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
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
@extend_schema(
    summary="List all accounts",
    description="Retrieve a list of all accounts with optional filtering by account group and search",
    parameters=[
        OpenApiParameter(name='account_group', type=OpenApiTypes.INT, description='Filter by account group ID'),
        OpenApiParameter(name='search', type=OpenApiTypes.STR, description='Search by account name')
    ],
    responses=AccountSerializer(many=True)
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
    ],
    responses=AccountSerializer
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
    request=AccountSerializer,
    responses=AccountSerializer
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


# Template-based views for frontend

@login_required
def pricelists_view(request):
    """
    Display list of pricelists with search functionality
    """
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'priceListName')  # Default sort by name
    sort_order = request.GET.get('order', 'asc')
    
    # Base queryset
    queryset = PriceList.objects.filter(isDeleted=False).select_related('createdBy', 'updatedBy')
    
    # Apply search filter
    if search_query:
        queryset = queryset.filter(
            Q(priceListName__icontains=search_query) |
            Q(id__icontains=search_query)
        )
    
    # Apply sorting
    if sort_order == 'desc':
        sort_by = f'-{sort_by}'
    queryset = queryset.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(queryset, 10)  # 10 items per page
    page_number = request.GET.get('page')
    pricelists = paginator.get_page(page_number)
    
    context = {
        'pricelists': pricelists,
        'search_query': search_query,
        'sort_by': request.GET.get('sort', 'priceListName'),
        'sort_order': sort_order,
    }
    
    return render(request, 'core/pricelists/list.html', context)

@login_required
def pricelist_add_view(request):
    """
    Add new pricelist
    """
    if request.method == 'POST':
        name = request.POST.get('priceListName', '').strip()
        
        if not name:
            messages.error(request, 'اسم قائمة السعر مطلوب')
        else:
            try:
                # Check if name already exists
                if PriceList.objects.filter(priceListName=name, isDeleted=False).exists():
                    messages.error(request, 'اسم قائمة السعر موجود بالفعل')
                else:
                    pricelist = PriceList.objects.create(
                        priceListName=name,
                        createdBy=request.user
                    )
                    messages.success(request, f'تم إضافة قائمة السعر "{name}" بنجاح')
                    return redirect('core:pricelists')
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء إضافة قائمة السعر: {str(e)}')
    
    return render(request, 'core/pricelists/add.html')

@login_required
def pricelist_edit_view(request, id):
    """
    Edit existing pricelist
    """
    pricelist = get_object_or_404(PriceList, id=id, isDeleted=False)
    
    if request.method == 'POST':
        name = request.POST.get('priceListName', '').strip()
        
        if not name:
            messages.error(request, 'اسم قائمة السعر مطلوب')
        else:
            try:
                # Check if name already exists (excluding current pricelist)
                if PriceList.objects.filter(priceListName=name, isDeleted=False).exclude(id=id).exists():
                    messages.error(request, 'اسم قائمة السعر موجود بالفعل')
                else:
                    pricelist.priceListName = name
                    pricelist.updatedBy = request.user
                    pricelist.save()
                    messages.success(request, f'تم تحديث قائمة السعر "{name}" بنجاح')
                    return redirect('core:pricelists')
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء تحديث قائمة السعر: {str(e)}')
    
    context = {
        'pricelist': pricelist,
    }
    
    return render(request, 'core/pricelists/edit.html', context)

@login_required
def pricelist_delete_view(request, id):
    """
    Delete pricelist (soft delete)
    """
    pricelist = get_object_or_404(PriceList, id=id, isDeleted=False)
    
    # Check if pricelist is referenced in PriceListDetail table
    if PriceListDetail.objects.filter(priceList=pricelist, isDeleted=False).exists():
        messages.error(request, 'لا يمكن حذف قائمة السعر لأنها مرتبطة بأسعار أصناف')
        return redirect('core:pricelists')
    
    if request.method == 'POST':
        try:
            pricelist.isDeleted = True
            pricelist.deletedBy = request.user
            pricelist.deletedAt = timezone.now()
            pricelist.updatedBy = request.user
            pricelist.save()
            messages.success(request, f'تم حذف قائمة السعر "{pricelist.priceListName}" بنجاح')
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف قائمة السعر: {str(e)}')
        
        return redirect('core:pricelists')
    
    context = {
        'pricelist': pricelist,
    }
    
    return render(request, 'core/pricelists/delete.html', context)


# StoreGroups template-based views for frontend

@login_required
def storegroups_view(request):
    """
    Display list of store groups with search functionality
    """
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'storeGroupName')  # Default sort by name
    sort_order = request.GET.get('order', 'asc')
    
    # Base queryset
    queryset = StoreGroup.objects.filter(isDeleted=False).select_related('createdBy', 'updatedBy')
    
    # Apply search filter
    if search_query:
        queryset = queryset.filter(
            Q(storeGroupName__icontains=search_query) |
            Q(id__icontains=search_query)
        )
    
    # Apply sorting
    if sort_order == 'desc':
        sort_by = f'-{sort_by}'
    queryset = queryset.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(queryset, 10)  # 10 items per page
    page_number = request.GET.get('page')
    storegroups = paginator.get_page(page_number)
    
    context = {
        'storegroups': storegroups,
        'search_query': search_query,
        'sort_by': request.GET.get('sort', 'storeGroupName'),
        'sort_order': sort_order,
    }
    
    return render(request, 'core/storegroups/list.html', context)

@login_required
def storegroup_add_view(request):
    """
    Add new store group
    """
    if request.method == 'POST':
        name = request.POST.get('storeGroupName', '').strip()
        
        if not name:
            messages.error(request, 'اسم مجموعة المخازن مطلوب')
        else:
            try:
                # Check if name already exists
                if StoreGroup.objects.filter(storeGroupName=name, isDeleted=False).exists():
                    messages.error(request, 'اسم مجموعة المخازن موجود بالفعل')
                else:
                    storegroup = StoreGroup.objects.create(
                        storeGroupName=name,
                        createdBy=request.user
                    )
                    messages.success(request, f'تم إضافة مجموعة المخازن "{name}" بنجاح')
                    return redirect('core:storegroups')
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء إضافة مجموعة المخازن: {str(e)}')
    
    return render(request, 'core/storegroups/add.html')

@login_required
def storegroup_edit_view(request, id):
    """
    Edit existing store group
    """
    storegroup = get_object_or_404(StoreGroup, id=id, isDeleted=False)
    
    if request.method == 'POST':
        name = request.POST.get('storeGroupName', '').strip()
        
        if not name:
            messages.error(request, 'اسم مجموعة المخازن مطلوب')
        else:
            try:
                # Check if name already exists (excluding current store group)
                if StoreGroup.objects.filter(storeGroupName=name, isDeleted=False).exclude(id=id).exists():
                    messages.error(request, 'اسم مجموعة المخازن موجود بالفعل')
                else:
                    storegroup.storeGroupName = name
                    storegroup.updatedBy = request.user
                    storegroup.save()
                    messages.success(request, f'تم تحديث مجموعة المخازن "{name}" بنجاح')
                    return redirect('core:storegroups')
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء تحديث مجموعة المخازن: {str(e)}')
    
    context = {
        'storegroup': storegroup,
    }
    
    return render(request, 'core/storegroups/edit.html', context)

@login_required
def storegroup_delete_view(request, id):
    """
    Delete store group (soft delete)
    """
    storegroup = get_object_or_404(StoreGroup, id=id, isDeleted=False)
    
    # Check if store group is referenced in Store table
    if Store.objects.filter(storeGroup=storegroup, isDeleted=False).exists():
        messages.error(request, 'لا يمكن حذف مجموعة المخازن لأنها مرتبطة بمخازن')
        return redirect('core:storegroups')
    
    if request.method == 'POST':
        try:
            storegroup.isDeleted = True
            storegroup.deletedBy = request.user
            storegroup.deletedAt = timezone.now()
            storegroup.updatedBy = request.user
            storegroup.save()
            messages.success(request, f'تم حذف مجموعة المخازن "{storegroup.storeGroupName}" بنجاح')
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف مجموعة المخازن: {str(e)}')
        
        return redirect('core:storegroups')
    
    context = {
        'storegroup': storegroup,
    }
    
    return render(request, 'core/storegroups/delete.html', context)


# =============================================
# STORES TEMPLATE-BASED VIEWS
# =============================================

@login_required
def stores_view(request):
    """
    Display list of stores with search functionality
    """
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'storeName')
    sort_direction = request.GET.get('direction', 'asc')
    
    # Validate sort fields
    valid_sort_fields = ['id', 'storeName', 'storeGroup', 'createdAt', 'updatedAt']
    if sort_by not in valid_sort_fields:
        sort_by = 'storeName'
    
    # Build sort field with direction
    if sort_direction == 'desc':
        sort_field = f'-{sort_by}'
    else:
        sort_field = sort_by
    
    # Base queryset
    stores = Store.objects.filter(isDeleted=False)
    
    # Apply search filter
    if search_query:
        stores = stores.filter(
            Q(storeName__icontains=search_query) |
            Q(storeGroup__icontains=search_query) |
            Q(id__icontains=search_query)
        )
    
    # Apply sorting
    stores = stores.order_by(sort_field)
    
    # Pagination
    paginator = Paginator(stores, 15)  # Show 15 stores per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'stores': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
        'sort_direction': sort_direction,
        'total_count': stores.count(),
    }
    
    return render(request, 'core/stores/list.html', context)


@login_required
def stores_add_view(request):
    """
    Add new store
    """
    if request.method == 'POST':
        store_name = request.POST.get('storeName', '').strip()
        store_group = request.POST.get('storeGroup', '').strip()
        
        # Validation
        if not store_name:
            messages.error(request, 'اسم المخزن مطلوب')
        elif len(store_name) > 255:
            messages.error(request, 'اسم المخزن لا يمكن أن يزيد عن 255 حرف')
        elif Store.objects.filter(storeName=store_name, isDeleted=False).exists():
            messages.error(request, 'يوجد مخزن بنفس الاسم بالفعل')
        else:
            try:
                # Create new store
                store = Store.objects.create(
                    storeName=store_name,
                    storeGroup=store_group if store_group else None,
                    createdBy=request.user,
                    updatedBy=request.user
                )
                
                messages.success(request, f'تم إضافة المخزن "{store_name}" بنجاح')
                return redirect('core:stores')
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء إضافة المخزن: {str(e)}')
    
    # Get store groups for dropdown
    store_groups = StoreGroup.objects.filter(isDeleted=False).order_by('storeGroupName')
    
    context = {
        'store_groups': store_groups,
    }
    
    return render(request, 'core/stores/add.html', context)


@login_required
def stores_edit_view(request, store_id):
    """
    Edit existing store
    """
    store = get_object_or_404(Store, id=store_id, isDeleted=False)
    
    if request.method == 'POST':
        store_name = request.POST.get('storeName', '').strip()
        store_group = request.POST.get('storeGroup', '').strip()
        
        # Validation
        if not store_name:
            messages.error(request, 'اسم المخزن مطلوب')
        elif len(store_name) > 255:
            messages.error(request, 'اسم المخزن لا يمكن أن يزيد عن 255 حرف')
        elif Store.objects.filter(storeName=store_name, isDeleted=False).exclude(id=store.id).exists():
            messages.error(request, 'يوجد مخزن بنفس الاسم بالفعل')
        else:
            try:
                # Update store
                store.storeName = store_name
                store.storeGroup = store_group if store_group else None
                store.updatedBy = request.user
                store.save()
                
                messages.success(request, f'تم تحديث المخزن "{store_name}" بنجاح')
                return redirect('core:stores')
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء تحديث المخزن: {str(e)}')
    
    # Get store groups for dropdown
    store_groups = StoreGroup.objects.filter(isDeleted=False).order_by('storeGroupName')
    
    context = {
        'store': store,
        'store_groups': store_groups,
    }
    
    return render(request, 'core/stores/edit.html', context)


@login_required
def stores_delete_view(request, store_id):
    """
    Delete store (soft delete)
    """
    store = get_object_or_404(Store, id=store_id, isDeleted=False)
    
    if request.method == 'POST':
        try:
            # Check if store is referenced in invoiceMaster
            # Note: This would need to be implemented when invoiceMaster model exists
            # For now, we'll proceed with the deletion
            
            # Soft delete
            store.isDeleted = True
            store.deletedBy = request.user
            store.updatedBy = request.user
            from django.utils import timezone
            store.deletedAt = timezone.now()
            store.save()
            
            messages.success(request, f'تم حذف المخزن "{store.storeName}" بنجاح')
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف المخزن: {str(e)}')
        
        return redirect('core:stores')
    
    context = {
        'store': store,
    }
    
    return render(request, 'core/stores/delete.html', context)


# =============================================
# ITEMS TEMPLATE-BASED VIEWS
# =============================================

@login_required
def items_view(request):
    """
    Display list of items with search functionality
    """
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'itemName')
    sort_direction = request.GET.get('direction', 'asc')
    
    # Validate sort fields
    valid_sort_fields = ['id', 'itemName', 'itemGroupId__itemsGroupName', 'sign', 'createdAt', 'updatedAt']
    if sort_by not in valid_sort_fields:
        sort_by = 'itemName'
    
    # Build sort field with direction
    if sort_direction == 'desc':
        sort_field = f'-{sort_by}'
    else:
        sort_field = sort_by
    
    # Base queryset
    items = Item.objects.select_related('itemGroupId').filter(isDeleted=False)
    
    # Apply search filter
    if search_query:
        items = items.filter(
            Q(itemName__icontains=search_query) |
            Q(itemGroupId__itemsGroupName__icontains=search_query) |
            Q(sign__icontains=search_query) |
            Q(id__icontains=search_query)
        )
    
    # Apply sorting
    items = items.order_by(sort_field)
    
    # Pagination
    paginator = Paginator(items, 15)  # Show 15 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'items': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
        'sort_direction': sort_direction,
        'total_count': items.count(),
        'item_groups': ItemsGroup.objects.filter(isDeleted=False).order_by('itemsGroupName'),
        'pricelists': PriceList.objects.filter(isDeleted=False).order_by('priceListName'),
    }
    
    return render(request, 'core/items/list.html', context)


@login_required
def items_add_view(request):
    """
    Add new item with pricelist detail (AJAX endpoint)
    """
    if request.method == 'POST':
        item_name = request.POST.get('itemName', '').strip()
        item_sign = request.POST.get('sign', '').strip()
        pricelist_id = request.POST.get('pricelistId')
        price = request.POST.get('price', '').strip()
        item_group_id = request.POST.get('itemGroupId')
        
        # Validation
        errors = []
        
        if not item_name:
            errors.append('اسم الصنف مطلوب')
        elif len(item_name) > 255:
            errors.append('اسم الصنف لا يمكن أن يزيد عن 255 حرف')
        elif Item.objects.filter(itemName=item_name, isDeleted=False).exists():
            errors.append('يوجد صنف بنفس الاسم بالفعل')
        
        # Optional item group validation
        item_group = None
        if item_group_id:
            try:
                item_group = ItemsGroup.objects.get(id=item_group_id, isDeleted=False)
            except ItemsGroup.DoesNotExist:
                errors.append('مجموعة الصنف غير موجودة')
        
        # Optional pricelist and price validation
        pricelist = None
        price_decimal = None
        
        if pricelist_id:
            try:
                pricelist = PriceList.objects.get(id=pricelist_id, isDeleted=False)
            except PriceList.DoesNotExist:
                errors.append('قائمة الأسعار غير موجودة')
        
        if price:
            try:
                price_decimal = Decimal(price)
                if price_decimal < 0:
                    errors.append('السعر لا يمكن أن يكون سالباً')
            except (ValueError, TypeError):
                errors.append('السعر يجب أن يكون رقماً صحيحاً')
        
        # If pricelist is provided, price must also be provided and vice versa
        if pricelist_id and not price:
            errors.append('إذا تم اختيار قائمة أسعار، يجب إدخال السعر')
        elif price and not pricelist_id:
            errors.append('إذا تم إدخال سعر، يجب اختيار قائمة أسعار')
        
        if errors:
            return JsonResponse({
                'success': False,
                'errors': errors
            }, json_dumps_params={'ensure_ascii': False})
        
        try:
            # Create new item
            item = Item.objects.create(
                itemGroupId=item_group,
                itemName=item_name,
                sign=item_sign if item_sign else None,
                createdBy=request.user,
                updatedBy=request.user
            )
            
            # Create pricelist detail entry only if both pricelist and price are provided
            if pricelist and price_decimal is not None:
                PriceListDetail.objects.create(
                    priceList=pricelist,
                    item=item,
                    price=price_decimal,
                    createdBy=request.user,
                    updatedBy=request.user
                )
            
            return JsonResponse({
                'success': True,
                'message': f'تم إضافة الصنف "{item_name}" بنجاح'
            }, json_dumps_params={'ensure_ascii': False})
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': [f'حدث خطأ أثناء إضافة الصنف: {str(e)}']
            }, json_dumps_params={'ensure_ascii': False})
    
    # For GET request, return form data
    item_groups = ItemsGroup.objects.filter(isDeleted=False).order_by('itemsGroupName')
    pricelists = PriceList.objects.filter(isDeleted=False).order_by('priceListName')
    
    return JsonResponse({
        'item_groups': [{'id': ig.id, 'name': ig.itemsGroupName} for ig in item_groups],
        'pricelists': [{'id': pl.id, 'name': pl.priceListName} for pl in pricelists]
    }, json_dumps_params={'ensure_ascii': False})


@login_required
def items_detail_view(request, item_id):
    """
    Display item details with tabs for main info, price lists, and store stock
    """
    from django.db import connection
    
    item = get_object_or_404(Item, id=item_id, isDeleted=False)
    
    # Get price list details for this item
    price_details = PriceListDetail.objects.select_related('priceList').filter(
        item=item, 
        isDeleted=False,
        priceList__isDeleted=False
    ).order_by('priceList__priceListName')
    
    # Get available price lists (not already assigned to this item)
    assigned_pricelist_ids = price_details.values_list('priceList_id', flat=True)
    available_pricelists = PriceList.objects.filter(isDeleted=False).exclude(
        id__in=assigned_pricelist_ids
    ).order_by('priceListName')
    
    # Get item groups for dropdown
    item_groups = ItemsGroup.objects.filter(isDeleted=False).order_by('itemsGroupName')

    # Get stock information from itemStock view
    store_stocks = []
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    s."storeName",
                    COALESCE(ist.stock, 0) as stock
                FROM stores s
                LEFT JOIN "itemStock" ist ON s.id = ist."storeID" AND ist.id = %s AND ist."isDeleted" = FALSE
                WHERE s."isDeleted" = FALSE
                ORDER BY s."storeName"
            ''', [item.id])
            
            for row in cursor.fetchall():
                store_stocks.append({
                    'store_name': row[0],
                    'stock': row[1]
                })
    except Exception as e:
        # If view doesn't exist or query fails, fall back to empty list
        print(f"Error querying itemStock view: {e}")
        pass
    
    context = {
        'item': item,
        'price_details': price_details,
        'available_pricelists': available_pricelists,
        'store_stocks': store_stocks,
        'item_groups': item_groups,
    }
    
    return render(request, 'core/items/detail.html', context)


@login_required
def items_add_price_view(request, item_id):
    """
    Add price to item for a specific price list (AJAX endpoint)
    """
    if request.method == 'POST':
        item = get_object_or_404(Item, id=item_id, isDeleted=False)
        
        pricelist_id = request.POST.get('price_list_id')
        price = request.POST.get('price', '').strip()
        
        # Validation
        if not pricelist_id:
            return JsonResponse({'success': False, 'error': 'قائمة الأسعار مطلوبة'})
        
        if not price:
            return JsonResponse({'success': False, 'error': 'السعر مطلوب'})
        
        try:
            pricelist = PriceList.objects.get(id=pricelist_id, isDeleted=False)
            price_decimal = Decimal(price)
            
            if price_decimal < 0:
                return JsonResponse({'success': False, 'error': 'السعر لا يمكن أن يكون سالباً'})
            
            # Check if price already exists
            if PriceListDetail.objects.filter(item=item, priceList=pricelist, isDeleted=False).exists():
                return JsonResponse({'success': False, 'error': 'السعر موجود بالفعل لهذه القائمة'})
            
            # Create price detail
            PriceListDetail.objects.create(
                priceList=pricelist,
                item=item,
                price=price_decimal,
                createdBy=request.user,
                updatedBy=request.user
            )
            
            return JsonResponse({'success': True, 'message': 'تم إضافة السعر بنجاح'})
            
        except PriceList.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'قائمة الأسعار غير موجودة'})
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'السعر يجب أن يكون رقماً صحيحاً'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'حدث خطأ: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'طريقة الطلب غير صحيحة'})


@login_required
def items_update_price_view(request, item_id, price_id):
    """
    Update existing price (AJAX endpoint)
    """
    if request.method == 'PUT':
        import json
        
        item = get_object_or_404(Item, id=item_id, isDeleted=False)
        price_detail = get_object_or_404(PriceListDetail, id=price_id, item=item, isDeleted=False)
        
        try:
            data = json.loads(request.body)
            new_price = data.get('price')
            
            if new_price is None:
                return JsonResponse({'success': False, 'error': 'السعر مطلوب'})
            
            price_decimal = Decimal(str(new_price))
            
            if price_decimal < 0:
                return JsonResponse({'success': False, 'error': 'السعر لا يمكن أن يكون سالباً'})
            
            price_detail.price = price_decimal
            price_detail.updatedBy = request.user
            price_detail.save()
            
            return JsonResponse({'success': True, 'message': 'تم تحديث السعر بنجاح'})
            
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'السعر يجب أن يكون رقماً صحيحاً'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'حدث خطأ: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'طريقة الطلب غير صحيحة'})


@login_required
def items_delete_price_view(request, item_id, price_id):
    """
    Delete price (soft delete) (AJAX endpoint)
    """
    if request.method == 'DELETE':
        item = get_object_or_404(Item, id=item_id, isDeleted=False)
        price_detail = get_object_or_404(PriceListDetail, id=price_id, item=item, isDeleted=False)
        
        try:
            price_detail.isDeleted = True
            price_detail.deletedBy = request.user
            price_detail.updatedBy = request.user
            from django.utils import timezone
            price_detail.deletedAt = timezone.now()
            price_detail.save()
            
            return JsonResponse({'success': True, 'message': 'تم حذف السعر بنجاح'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'حدث خطأ: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'طريقة الطلب غير صحيحة'})


@login_required
def items_update_main_info_view(request, item_id):
    """
    Update item main information (AJAX endpoint)
    """
    if request.method == 'POST':
        item = get_object_or_404(Item, id=item_id, isDeleted=False)
        
        try:
            # Get form data
            item_name = request.POST.get('itemName', '').strip()
            item_group_id = request.POST.get('itemGroupId')
            is_used = request.POST.get('isUsed') == 'true'
            is_tax = request.POST.get('isTax') == 'true'
            barcode = request.POST.get('barcode', '').strip()
            sign = request.POST.get('sign', '').strip()
            item_image = request.POST.get('itemImage', '').strip()
            
            # Unit fields
            main_unit_name = request.POST.get('mainUnitName', '').strip()
            main_unit_barcode = request.POST.get('mainUnitBarcode', '').strip()
            sub_unit_name = request.POST.get('subUnitName', '').strip()
            sub_unit_pack = request.POST.get('subUnitPack', '0')
            sub_unit_barcode = request.POST.get('subUnitBarCode', '').strip()
            small_unit_name = request.POST.get('smallUnitName', '').strip()
            main_unit_pack = request.POST.get('mainUnitPack', '0')
            small_unit_barcode = request.POST.get('smallUnitBarCode', '').strip()
            
            # Validation
            if not item_name:
                return JsonResponse({'success': False, 'error': 'اسم العنصر مطلوب'})
            
            if len(item_name) > 255:
                return JsonResponse({'success': False, 'error': 'اسم العنصر لا يمكن أن يزيد عن 255 حرف'})
            
            # Check for duplicate item name
            if Item.objects.filter(itemName=item_name, isDeleted=False).exclude(id=item.id).exists():
                return JsonResponse({'success': False, 'error': 'يوجد عنصر بنفس الاسم بالفعل'})
            
            # Get item group (optional)
            item_group = None
            if item_group_id:
                try:
                    item_group = ItemsGroup.objects.get(id=item_group_id, isDeleted=False)
                except ItemsGroup.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'المجموعة غير موجودة'})
            
            # Validate numeric fields
            try:
                sub_unit_pack_decimal = Decimal(sub_unit_pack) if sub_unit_pack else 0
                main_unit_pack_decimal = Decimal(main_unit_pack) if main_unit_pack else 0
            except (ValueError, TypeError):
                return JsonResponse({'success': False, 'error': 'قيم العبوة يجب أن تكون أرقاماً صحيحة'})
            
            # Update item
            item.itemName = item_name
            item.itemGroupId = item_group
            item.isUsed = is_used
            item.isTax = is_tax
            item.barcode = barcode if barcode else None
            item.sign = sign if sign else None
            item.itemImage = item_image if item_image else None
            
            # Update unit information
            item.mainUnitName = main_unit_name if main_unit_name else None
            item.subUnitName = sub_unit_name if sub_unit_name else None
            item.smallUnitName = small_unit_name if small_unit_name else None
            item.subUnitPack = sub_unit_pack_decimal
            item.mainUnitPack = main_unit_pack_decimal
            item.subUnitBarCode = sub_unit_barcode if sub_unit_barcode else None
            item.smallUnitBarCode = small_unit_barcode if small_unit_barcode else None
            
            item.updatedBy = request.user
            item.save()
            
            return JsonResponse({'success': True, 'message': 'تم حفظ التغييرات بنجاح'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'حدث خطأ: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'طريقة الطلب غير صحيحة'})


@login_required
def items_edit_view(request, item_id):
    """
    Edit existing item
    """
    item = get_object_or_404(Item, id=item_id, isDeleted=False)
    
    if request.method == 'POST':
        item_name = request.POST.get('itemName', '').strip()
        item_sign = request.POST.get('sign', '').strip()
        item_group_id = request.POST.get('itemGroupId')
        
        # Validation
        if not item_name:
            messages.error(request, 'اسم الصنف مطلوب')
        elif len(item_name) > 255:
            messages.error(request, 'اسم الصنف لا يمكن أن يزيد عن 255 حرف')
        elif Item.objects.filter(itemName=item_name, isDeleted=False).exclude(id=item.id).exists():
            messages.error(request, 'يوجد صنف بنفس الاسم بالفعل')
        else:
            try:
                # Get item group (optional)
                item_group = None
                if item_group_id:
                    item_group = get_object_or_404(ItemsGroup, id=item_group_id, isDeleted=False)
                
                # Update item
                item.itemName = item_name
                item.sign = item_sign if item_sign else None
                item.itemGroupId = item_group
                item.updatedBy = request.user
                item.save()
                
                messages.success(request, f'تم تحديث الصنف "{item_name}" بنجاح')
                return redirect('core:items')
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء تحديث الصنف: {str(e)}')
    
    # Get item groups for dropdown
    item_groups = ItemsGroup.objects.filter(isDeleted=False).order_by('itemsGroupName')
    
    context = {
        'item': item,
        'item_groups': item_groups,
    }
    
    return render(request, 'core/items/edit.html', context)


@login_required
def items_upload_image_view(request):
    """
    Upload image for item (AJAX endpoint)
    """
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            import os
            from django.core.files.storage import default_storage
            from django.conf import settings
            import uuid
            
            image_file = request.FILES['image']
            
            # Validate file type
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            file_extension = image_file.name.split('.')[-1].lower()
            
            if file_extension not in allowed_extensions:
                return JsonResponse({
                    'success': False,
                    'error': 'نوع الملف غير مدعوم. يُسمح بـ: JPG, PNG, GIF, WEBP'
                }, json_dumps_params={'ensure_ascii': False})
            
            # Validate file size (max 5MB)
            if image_file.size > 5 * 1024 * 1024:
                return JsonResponse({
                    'success': False,
                    'error': 'حجم الملف كبير جداً. الحد الأقصى 5 ميجابايت'
                }, json_dumps_params={'ensure_ascii': False})
            
            # Generate unique filename
            unique_filename = f"items/{uuid.uuid4().hex}.{file_extension}"
            
            # Save file
            file_path = default_storage.save(unique_filename, image_file)
            
            # Return URL
            file_url = f"{settings.MEDIA_URL}{file_path}"
            
            return JsonResponse({
                'success': True,
                'url': file_url,
                'message': 'تم رفع الصورة بنجاح'
            }, json_dumps_params={'ensure_ascii': False})
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'حدث خطأ أثناء رفع الصورة: {str(e)}'
            }, json_dumps_params={'ensure_ascii': False})
    
    return JsonResponse({
        'success': False,
        'error': 'طريقة الطلب غير صحيحة أو لا يوجد ملف'
    }, json_dumps_params={'ensure_ascii': False})


@login_required
def items_delete_view(request, item_id):
    """
    Delete item (soft delete) - check if used in invoiceDetails or priceListsDetails
    """
    item = get_object_or_404(Item, id=item_id, isDeleted=False)
    
    if request.method == 'POST':
        try:
            # Check if item is used in InvoiceDetail
            if hasattr(item, 'invoicedetail_set') and item.invoicedetail_set.filter(isDeleted=False).exists():
                messages.error(request, f'لا يمكن حذف الصنف "{item.itemName}" لأنه مستخدم في فواتير')
                return redirect('core:items')
            
            # Allow deletion even if item is bound to price lists
            # When deleting item, also soft delete associated price list details
            if hasattr(item, 'pricelistdetail_set'):
                price_details = item.pricelistdetail_set.filter(isDeleted=False)
                for price_detail in price_details:
                    price_detail.isDeleted = True
                    price_detail.deletedBy = request.user
                    price_detail.updatedBy = request.user
                    price_detail.deletedAt = timezone.now()
                    price_detail.save()
            
            # Soft delete the item
            item.isDeleted = True
            item.deletedBy = request.user
            item.updatedBy = request.user
            item.deletedAt = timezone.now()
            item.save()
            
            messages.success(request, f'تم حذف الصنف "{item.itemName}" بنجاح')
            return redirect('core:items')
            
        except Exception as e:
            # More detailed error information for debugging
            import traceback
            error_details = traceback.format_exc()
            print(f"Error deleting item {item.id}: {error_details}")  # For server logs
            messages.error(request, f'حدث خطأ أثناء حذف الصنف: {str(e)}')
            return redirect('core:items')
    
    # Check usage for display
    invoice_usage = hasattr(item, 'invoicedetail_set') and item.invoicedetail_set.filter(isDeleted=False).exists()
    pricelist_usage = hasattr(item, 'pricelistdetail_set') and item.pricelistdetail_set.filter(isDeleted=False).exists()
    
    context = {
        'item': item,
        'invoice_usage': invoice_usage,
        'pricelist_usage': pricelist_usage,
        'can_delete': not invoice_usage  # Only prevent deletion if used in invoices
    }
    
    return render(request, 'core/items/delete.html', context)


# =============================================
# ITEMSGROUPS TEMPLATE-BASED VIEWS
# =============================================

@login_required
def itemsgroups_view(request):
    """
    Display list of items groups with search functionality
    """
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'itemsGroupName')
    sort_direction = request.GET.get('direction', 'asc')
    
    # Validate sort fields
    valid_sort_fields = ['id', 'itemsGroupName', 'createdAt', 'updatedAt']
    if sort_by not in valid_sort_fields:
        sort_by = 'itemsGroupName'
    
    # Build sort field with direction
    if sort_direction == 'desc':
        sort_field = f'-{sort_by}'
    else:
        sort_field = sort_by
    
    # Base queryset
    items_groups = ItemsGroup.objects.select_related('createdBy', 'updatedBy').filter(isDeleted=False)
    
    # Apply search filter
    if search_query:
        items_groups = items_groups.filter(
            Q(itemsGroupName__icontains=search_query) |
            Q(id__icontains=search_query)
        )
    
    # Apply sorting
    items_groups = items_groups.order_by(sort_field)
    
    # Pagination
    paginator = Paginator(items_groups, 15)  # Show 15 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'items_groups': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
        'sort_direction': sort_direction,
        'total_count': items_groups.count(),
    }
    
    return render(request, 'core/itemsgroups/list.html', context)


@login_required
def itemsgroups_add_view(request):
    """
    Add new items group (AJAX endpoint)
    """
    if request.method == 'POST':
        group_name = request.POST.get('itemsGroupName', '').strip()
        
        # Validation
        errors = []
        
        if not group_name:
            errors.append('اسم مجموعة الأصناف مطلوب')
        elif len(group_name) > 255:
            errors.append('اسم مجموعة الأصناف لا يمكن أن يزيد عن 255 حرف')
        elif ItemsGroup.objects.filter(itemsGroupName=group_name, isDeleted=False).exists():
            errors.append('يوجد مجموعة أصناف بنفس الاسم بالفعل')
        
        if errors:
            return JsonResponse({
                'success': False,
                'errors': errors
            })
        
        try:
            # Create new items group
            items_group = ItemsGroup.objects.create(
                itemsGroupName=group_name,
                createdBy=request.user,
                updatedBy=request.user
            )
            
            return JsonResponse({
                'success': True,
                'message': f'تم إضافة مجموعة الأصناف "{group_name}" بنجاح'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': [f'حدث خطأ أثناء إضافة مجموعة الأصناف: {str(e)}']
            })
    
    return JsonResponse({'success': False, 'error': 'طريقة الطلب غير صحيحة'})


@login_required
def itemsgroups_edit_view(request, group_id):
    """
    Edit existing items group
    """
    itemsgroup = get_object_or_404(ItemsGroup, id=group_id, isDeleted=False)
    
    # Count items in this group
    items_count = Item.objects.filter(itemGroupId=itemsgroup, isDeleted=False).count()
    
    if request.method == 'POST':
        group_name = request.POST.get('itemsGroupName', '').strip()
        
        # Validation
        if not group_name:
            messages.error(request, 'اسم مجموعة الأصناف مطلوب')
        elif len(group_name) > 255:
            messages.error(request, 'اسم مجموعة الأصناف لا يمكن أن يزيد عن 255 حرف')
        elif ItemsGroup.objects.filter(itemsGroupName=group_name, isDeleted=False).exclude(id=itemsgroup.id).exists():
            messages.error(request, 'يوجد مجموعة أصناف بنفس الاسم بالفعل')
        else:
            try:
                # Update items group
                itemsgroup.itemsGroupName = group_name
                itemsgroup.updatedBy = request.user
                itemsgroup.save()
                
                messages.success(request, f'تم تحديث مجموعة الأصناف "{group_name}" بنجاح')
                return redirect('core:itemsgroups')
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء تحديث مجموعة الأصناف: {str(e)}')
    
    context = {
        'itemsgroup': itemsgroup,
        'items_count': items_count,
    }
    
    return render(request, 'core/itemsgroups/edit.html', context)


@login_required
def itemsgroups_delete_view(request, group_id):
    """
    Delete items group (soft delete)
    """
    itemsgroup = get_object_or_404(ItemsGroup, id=group_id, isDeleted=False)
    
    # Get items linked to this group
    linked_items = Item.objects.filter(itemGroupId=itemsgroup, isDeleted=False)
    items_count = linked_items.count()
    
    if request.method == 'POST':
        try:
            # Check if items group is referenced in items table
            if items_count > 0:
                messages.error(request, f'لا يمكن حذف مجموعة الأصناف "{itemsgroup.itemsGroupName}" لأنها مرتبطة بـ {items_count} صنف')
                return redirect('core:itemsgroups')
            
            # Soft delete
            itemsgroup.isDeleted = True
            itemsgroup.deletedBy = request.user
            itemsgroup.updatedBy = request.user
            # deletedAt will be set automatically due to auto_now=True on updatedAt
            from django.utils import timezone
            itemsgroup.deletedAt = timezone.now()
            itemsgroup.save()
            
            messages.success(request, f'تم حذف مجموعة الأصناف "{itemsgroup.itemsGroupName}" بنجاح')
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف مجموعة الأصناف: {str(e)}')
        
        return redirect('core:itemsgroups')
    
    context = {
        'itemsgroup': itemsgroup,
        'items_count': items_count,
        'linked_items': linked_items[:10],  # Show first 10 linked items
    }
    
    return render(request, 'core/itemsgroups/delete.html', context)


# =============================================
# CUSTOMERS TEMPLATE-BASED VIEWS
# =============================================

@login_required
def customers_view(request):
    """
    Display list of customers (type=1 or type=3) with search functionality
    """
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'customerVendorName')
    sort_direction = request.GET.get('direction', 'asc')
    
    # Validate sort fields
    valid_sort_fields = ['id', 'customerVendorName', 'phone_one', 'createdAt', 'updatedAt']
    if sort_by not in valid_sort_fields:
        sort_by = 'customerVendorName'
    
    # Build sort field with direction
    if sort_direction == 'desc':
        sort_field = f'-{sort_by}'
    else:
        sort_field = sort_by
    
    # Base queryset - customers only (type 1 or 3)
    customers = CustomerVendor.objects.select_related('createdBy', 'updatedBy').filter(
        isDeleted=False,
        type__in=[1, 3]  # Customer or Both
    )
    
    # Apply search filter
    if search_query:
        customers = customers.filter(
            Q(customerVendorName__icontains=search_query) |
            Q(phone_one__icontains=search_query) |
            Q(phone_two__icontains=search_query) |
            Q(notes__icontains=search_query) |
            Q(id__icontains=search_query)
        )
    
    # Apply sorting
    customers = customers.order_by(sort_field)
    
    # Add can_delete property for each customer
    for customer in customers:
        # Check if customer is referenced in invoiceMaster or transactions
        customer.can_delete = not (
            InvoiceMaster.objects.filter(customerOrVendorID=customer, isDeleted=False).exists() or
            Transaction.objects.filter(customerVendorID=customer, isDeleted=False).exists()
        )
    
    # Pagination
    paginator = Paginator(customers, 15)  # Show 15 customers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'customers': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
        'sort_direction': sort_direction,
        'total_count': customers.count(),
    }
    
    return render(request, 'core/customers/list.html', context)


@login_required
def customers_add_view(request):
    """
    Add new customer
    """
    if request.method == 'POST':
        customer_name = request.POST.get('customerVendorName', '').strip()
        phone_one = request.POST.get('phone_one', '').strip()
        phone_two = request.POST.get('phone_two', '').strip()
        notes = request.POST.get('notes', '').strip()
        default_price_list_id = request.POST.get('default_price_list', '').strip()
        
        # Validation
        if not customer_name:
            messages.error(request, 'اسم العميل مطلوب')
        elif len(customer_name) > 255:
            messages.error(request, 'اسم العميل لا يمكن أن يزيد عن 255 حرف')
        else:
            try:
                # Create new customer (type=1 for Customer)
                customer = CustomerVendor.objects.create(
                    customerVendorName=customer_name,
                    phone_one=phone_one if phone_one else None,
                    phone_two=phone_two if phone_two else None,
                    notes=notes if notes else None,
                    type=1,  # Customer type
                    createdBy=request.user,
                    updatedBy=request.user
                )
                
                # Create price list association if selected
                if default_price_list_id:
                    try:
                        price_list = PriceList.objects.get(id=default_price_list_id, isDeleted=False)
                        CustomerVendorPriceList.objects.create(
                            customerVendorID=customer,
                            priceListID=price_list,
                            createdBy=request.user,
                            updatedBy=request.user
                        )
                    except PriceList.DoesNotExist:
                        messages.warning(request, 'قائمة الأسعار المحددة غير موجودة')
                
                messages.success(request, f'تم إضافة العميل "{customer_name}" بنجاح')
                return redirect('core:customers')
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء إضافة العميل: {str(e)}')
    
    # Get all available price lists for the dropdown
    price_lists = PriceList.objects.filter(isDeleted=False).order_by('priceListName')
    
    # For GET request or form errors, show form with preserved data
    form_data = request.POST if request.method == 'POST' else {}
    context = {
        'form_data': form_data,
        'price_lists': price_lists,
    }
    
    return render(request, 'core/customers/add.html', context)


@login_required
def customers_edit_view(request, customer_id):
    """
    Edit existing customer
    """
    customer = get_object_or_404(CustomerVendor, id=customer_id, isDeleted=False, type__in=[1, 3])
    
    if request.method == 'POST':
        customer_name = request.POST.get('customerVendorName', '').strip()
        phone_one = request.POST.get('phone_one', '').strip()
        phone_two = request.POST.get('phone_two', '').strip()
        notes = request.POST.get('notes', '').strip()
        default_price_list_id = request.POST.get('default_price_list', '').strip()
        
        # Validation
        if not customer_name:
            messages.error(request, 'اسم العميل مطلوب')
        elif len(customer_name) > 255:
            messages.error(request, 'اسم العميل لا يمكن أن يزيد عن 255 حرف')
        else:
            try:
                # Update customer
                customer.customerVendorName = customer_name
                customer.phone_one = phone_one if phone_one else None
                customer.phone_two = phone_two if phone_two else None
                customer.notes = notes if notes else None
                customer.updatedBy = request.user
                customer.save()
                
                # Update price list association if selected
                if default_price_list_id:
                    try:
                        price_list = PriceList.objects.get(id=default_price_list_id, isDeleted=False)
                        # Remove existing associations
                        CustomerVendorPriceList.objects.filter(customerVendorID=customer).delete()
                        # Create new association
                        CustomerVendorPriceList.objects.create(
                            customerVendorID=customer,
                            priceListID=price_list,
                            createdBy=request.user,
                            updatedBy=request.user
                        )
                    except PriceList.DoesNotExist:
                        messages.warning(request, 'قائمة الأسعار المحددة غير موجودة')
                else:
                    # Remove existing associations if no price list selected
                    CustomerVendorPriceList.objects.filter(customerVendorID=customer).delete()
                
                messages.success(request, f'تم تحديث العميل "{customer_name}" بنجاح')
                return redirect('core:customers')
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء تحديث العميل: {str(e)}')
    
    # Get all available price lists for the dropdown
    price_lists = PriceList.objects.filter(isDeleted=False).order_by('priceListName')
    
    # Get current default price list for this customer
    current_price_list = None
    try:
        customer_price_list = CustomerVendorPriceList.objects.get(customerVendorID=customer, isDeleted=False)
        current_price_list = customer_price_list.priceListID
    except CustomerVendorPriceList.DoesNotExist:
        pass
    
    # Add current price list id to customer object for template
    customer.default_price_list_id = current_price_list.id if current_price_list else None
    
    context = {
        'customer': customer,
        'price_lists': price_lists,
        'current_price_list': current_price_list,
    }
    
    return render(request, 'core/customers/edit.html', context)


@login_required
def customers_delete_view(request, customer_id):
    """
    Delete customer (soft delete)
    """
    customer = get_object_or_404(CustomerVendor, id=customer_id, isDeleted=False, type__in=[1, 3])
    
    # Check if customer can be deleted
    customer.can_delete = not (
        InvoiceMaster.objects.filter(customerOrVendorID=customer, isDeleted=False).exists() or
        Transaction.objects.filter(customerVendorID=customer, isDeleted=False).exists()
    )
    
    if request.method == 'POST' and customer.can_delete:
        try:
            # Soft delete
            customer.isDeleted = True
            customer.deletedBy = request.user
            customer.updatedBy = request.user
            from django.utils import timezone
            customer.deletedAt = timezone.now()
            customer.save()
            
            messages.success(request, f'تم حذف العميل "{customer.customerVendorName}" بنجاح')
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف العميل: {str(e)}')
        
        return redirect('core:customers')
    
    context = {
        'customer': customer,
    }
    
    return render(request, 'core/customers/delete.html', context)


# ==================== VENDOR MANAGEMENT VIEWS ====================

@login_required
def vendors_view(request):
    """
    Display vendors list with search and pagination
    """
    vendors = CustomerVendor.objects.filter(isDeleted=False, type__in=[2, 3]).order_by('-id')
    
    # Get search parameters
    search_query = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'customerVendorName')
    sort_direction = request.GET.get('direction', 'asc')
    
    # Apply search filter
    if search_query:
        vendors = vendors.filter(
            Q(customerVendorName__icontains=search_query) |
            Q(phone_one__icontains=search_query) |
            Q(phone_two__icontains=search_query) |
            Q(notes__icontains=search_query)
        )
    
    # Apply sorting
    valid_sort_fields = ['customerVendorName', 'id', 'phone_one', 'createdAt', 'updatedAt']
    if sort_by in valid_sort_fields:
        if sort_direction == 'desc':
            sort_by = '-' + sort_by
        vendors = vendors.order_by(sort_by)
    
    # Add deletion capability check
    for vendor in vendors:
        vendor.can_delete = not (
            InvoiceMaster.objects.filter(customerOrVendorID=vendor, isDeleted=False).exists() or
            Transaction.objects.filter(customerVendorID=vendor, isDeleted=False).exists()
        )
    
    # Pagination
    paginator = Paginator(vendors, 15)  # 15 vendors per page
    page_number = request.GET.get('page')
    vendors_page = paginator.get_page(page_number)
    
    context = {
        'vendors': vendors_page,
        'search_query': search_query,
        'sort_by': request.GET.get('sort', 'customerVendorName'),
        'sort_direction': sort_direction,
        'total_count': paginator.count,
    }
    
    return render(request, 'core/vendors/list.html', context)


@login_required
def vendors_add_view(request):
    """
    Add new vendor
    """
    if request.method == 'POST':
        vendor_name = request.POST.get('customerVendorName', '').strip()
        phone_one = request.POST.get('phone_one', '').strip()
        phone_two = request.POST.get('phone_two', '').strip()
        notes = request.POST.get('notes', '').strip()
        default_price_list_id = request.POST.get('default_price_list', '').strip()
        
        # Validation
        if not vendor_name:
            messages.error(request, 'اسم المورد مطلوب')
        elif len(vendor_name) > 255:
            messages.error(request, 'اسم المورد لا يمكن أن يزيد عن 255 حرف')
        else:
            try:
                # Create new vendor (type=2 for Vendor)
                vendor = CustomerVendor.objects.create(
                    customerVendorName=vendor_name,
                    phone_one=phone_one if phone_one else None,
                    phone_two=phone_two if phone_two else None,
                    notes=notes if notes else None,
                    type=2,  # Vendor type
                    createdBy=request.user,
                    updatedBy=request.user
                )
                
                # Create price list association if selected
                if default_price_list_id:
                    try:
                        price_list = PriceList.objects.get(id=default_price_list_id, isDeleted=False)
                        CustomerVendorPriceList.objects.create(
                            customerVendorID=vendor,
                            priceListID=price_list,
                            createdBy=request.user,
                            updatedBy=request.user
                        )
                    except PriceList.DoesNotExist:
                        messages.warning(request, 'قائمة الأسعار المحددة غير موجودة')
                
                messages.success(request, f'تم إضافة المورد "{vendor_name}" بنجاح')
                return redirect('core:vendors')
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء إضافة المورد: {str(e)}')
    
    # Get all available price lists for the dropdown
    price_lists = PriceList.objects.filter(isDeleted=False).order_by('priceListName')
    
    # For GET request or form errors, show form with preserved data
    form_data = request.POST if request.method == 'POST' else {}
    context = {
        'form_data': form_data,
        'price_lists': price_lists,
    }
    
    return render(request, 'core/vendors/add.html', context)


@login_required
def vendors_edit_view(request, vendor_id):
    """
    Edit existing vendor
    """
    vendor = get_object_or_404(CustomerVendor, id=vendor_id, isDeleted=False, type__in=[2, 3])
    
    if request.method == 'POST':
        vendor_name = request.POST.get('customerVendorName', '').strip()
        phone_one = request.POST.get('phone_one', '').strip()
        phone_two = request.POST.get('phone_two', '').strip()
        notes = request.POST.get('notes', '').strip()
        default_price_list_id = request.POST.get('default_price_list', '').strip()
        
        # Validation
        if not vendor_name:
            messages.error(request, 'اسم المورد مطلوب')
        elif len(vendor_name) > 255:
            messages.error(request, 'اسم المورد لا يمكن أن يزيد عن 255 حرف')
        else:
            try:
                # Update vendor
                vendor.customerVendorName = vendor_name
                vendor.phone_one = phone_one if phone_one else None
                vendor.phone_two = phone_two if phone_two else None
                vendor.notes = notes if notes else None
                vendor.updatedBy = request.user
                vendor.save()
                
                # Update price list association if selected
                if default_price_list_id:
                    try:
                        price_list = PriceList.objects.get(id=default_price_list_id, isDeleted=False)
                        # Remove existing associations
                        CustomerVendorPriceList.objects.filter(customerVendorID=vendor).delete()
                        # Create new association
                        CustomerVendorPriceList.objects.create(
                            customerVendorID=vendor,
                            priceListID=price_list,
                            createdBy=request.user,
                            updatedBy=request.user
                        )
                    except PriceList.DoesNotExist:
                        messages.warning(request, 'قائمة الأسعار المحددة غير موجودة')
                else:
                    # Remove existing associations if no price list selected
                    CustomerVendorPriceList.objects.filter(customerVendorID=vendor).delete()
                
                messages.success(request, f'تم تحديث المورد "{vendor_name}" بنجاح')
                return redirect('core:vendors')
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء تحديث المورد: {str(e)}')
    
    # Get all available price lists for the dropdown
    price_lists = PriceList.objects.filter(isDeleted=False).order_by('priceListName')
    
    # Get current default price list for this vendor
    current_price_list = None
    try:
        vendor_price_list = CustomerVendorPriceList.objects.get(customerVendorID=vendor, isDeleted=False)
        current_price_list = vendor_price_list.priceListID
    except CustomerVendorPriceList.DoesNotExist:
        pass
    
    # Add current price list id to vendor object for template
    vendor.default_price_list_id = current_price_list.id if current_price_list else None
    
    context = {
        'vendor': vendor,
        'price_lists': price_lists,
        'current_price_list': current_price_list,
    }
    
    return render(request, 'core/vendors/edit.html', context)


@login_required
def vendors_delete_view(request, vendor_id):
    """
    Delete vendor (soft delete)
    """
    vendor = get_object_or_404(CustomerVendor, id=vendor_id, isDeleted=False, type__in=[2, 3])
    
    # Check if vendor can be deleted
    can_delete = not (
        InvoiceMaster.objects.filter(customerOrVendorID=vendor, isDeleted=False).exists() or
        Transaction.objects.filter(customerVendorID=vendor, isDeleted=False).exists()
    )
    
    # Count related records for display
    invoice_count = InvoiceMaster.objects.filter(customerOrVendorID=vendor, isDeleted=False).count()
    transaction_count = Transaction.objects.filter(customerVendorID=vendor, isDeleted=False).count()
    
    if request.method == 'POST' and can_delete:
        try:
            # Soft delete
            vendor.isDeleted = True
            vendor.deletedBy = request.user
            vendor.updatedBy = request.user
            from django.utils import timezone
            vendor.deletedAt = timezone.now()
            vendor.save()
            
            messages.success(request, f'تم حذف المورد "{vendor.customerVendorName}" بنجاح')
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف المورد: {str(e)}')
        
        return redirect('core:vendors')
    
    context = {
        'vendor': vendor,
        'can_delete': can_delete,
        'invoice_count': invoice_count,
        'transaction_count': transaction_count,
    }
    
    return render(request, 'core/vendors/delete.html', context)


# ============================================================================
# INVOICE MANAGEMENT VIEWS
# ============================================================================

@login_required
def invoices_purchase_view(request):
    """
    View Purchase invoices with filtering and sorting
    """
    # Get query parameters
    search = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'createdAt')
    sort_order = request.GET.get('sort_order', 'desc')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    created_by_filter = request.GET.get('created_by', '')
    
    # Build queryset for Purchase invoices (type=1)
    queryset = InvoiceMaster.objects.filter(
        invoiceType=1,  # Purchase invoices
        isDeleted=False
    ).select_related('customerOrVendorID', 'storeID', 'createdBy')
    
    # Apply search filter
    if search:
        queryset = queryset.filter(
            Q(id__icontains=search) |
            Q(customerOrVendorID__customerVendorName__icontains=search) |
            Q(notes__icontains=search)
        )
    
    # Apply date filters
    if date_from:
        queryset = queryset.filter(createdAt__date__gte=date_from)
    if date_to:
        queryset = queryset.filter(createdAt__date__lte=date_to)
    
    # Apply created by filter
    if created_by_filter:
        queryset = queryset.filter(
            Q(createdBy__id=created_by_filter) |
            Q(createdBy__username__icontains=created_by_filter)
        )
    
    # Apply sorting
    if sort_order == 'desc':
        sort_by = f'-{sort_by}'
    queryset = queryset.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all users for filter dropdown
    users = User.objects.filter(is_active=True).order_by('username')
    
    context = {
        'invoices': page_obj,
        'search': search,
        'sort_by': sort_by.lstrip('-'),
        'sort_order': sort_order,
        'date_from': date_from,
        'date_to': date_to,
        'created_by_filter': created_by_filter,
        'users': users,
        'invoice_type': 'purchase',
        'invoice_type_name': 'فواتير الشراء',
    }
    
    return render(request, 'core/invoices/purchase.html', context)


@login_required
def invoices_sales_view(request):
    """
    View Sales invoices with filtering and sorting
    """
    # Get query parameters
    search = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'createdAt')
    sort_order = request.GET.get('sort_order', 'desc')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    created_by_filter = request.GET.get('created_by', '')
    
    # Build queryset for Sales invoices (type=2)
    queryset = InvoiceMaster.objects.filter(
        invoiceType=2,  # Sales invoices
        isDeleted=False
    ).select_related('customerOrVendorID', 'storeID', 'createdBy')
    
    # Apply search filter
    if search:
        queryset = queryset.filter(
            Q(id__icontains=search) |
            Q(customerOrVendorID__customerVendorName__icontains=search) |
            Q(notes__icontains=search)
        )
    
    # Apply date filters
    if date_from:
        queryset = queryset.filter(createdAt__date__gte=date_from)
    if date_to:
        queryset = queryset.filter(createdAt__date__lte=date_to)
    
    # Apply created by filter
    if created_by_filter:
        queryset = queryset.filter(
            Q(createdBy__id=created_by_filter) |
            Q(createdBy__username__icontains=created_by_filter)
        )
    
    # Apply sorting
    if sort_order == 'desc':
        sort_by = f'-{sort_by}'
    queryset = queryset.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all users for filter dropdown
    users = User.objects.filter(is_active=True).order_by('username')
    
    context = {
        'invoices': page_obj,
        'search': search,
        'sort_by': sort_by.lstrip('-'),
        'sort_order': sort_order,
        'date_from': date_from,
        'date_to': date_to,
        'created_by_filter': created_by_filter,
        'users': users,
        'invoice_type': 'sales',
        'invoice_type_name': 'فواتير المبيعات',
    }
    
    return render(request, 'core/invoices/sales.html', context)


@login_required
def invoices_return_purchase_view(request):
    """
    View Return Purchase invoices with filtering and sorting
    """
    # Get query parameters
    search = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'createdAt')
    sort_order = request.GET.get('sort_order', 'desc')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    created_by_filter = request.GET.get('created_by', '')
    
    # Build queryset for Return Purchase invoices (type=3)
    queryset = InvoiceMaster.objects.filter(
        invoiceType=3,  # Return Purchase invoices
        isDeleted=False
    ).select_related('customerOrVendorID', 'storeID', 'createdBy', 'originalInvoiceID')
    
    # Apply search filter
    if search:
        queryset = queryset.filter(
            Q(id__icontains=search) |
            Q(customerOrVendorID__customerVendorName__icontains=search) |
            Q(notes__icontains=search) |
            Q(originalInvoiceID__id__icontains=search)
        )
    
    # Apply date filters
    if date_from:
        queryset = queryset.filter(createdAt__date__gte=date_from)
    if date_to:
        queryset = queryset.filter(createdAt__date__lte=date_to)
    
    # Apply created by filter
    if created_by_filter:
        queryset = queryset.filter(
            Q(createdBy__id=created_by_filter) |
            Q(createdBy__username__icontains=created_by_filter)
        )
    
    # Apply sorting
    if sort_order == 'desc':
        sort_by = f'-{sort_by}'
    queryset = queryset.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all users for filter dropdown
    users = User.objects.filter(is_active=True).order_by('username')
    
    context = {
        'invoices': page_obj,
        'search': search,
        'sort_by': sort_by.lstrip('-'),
        'sort_order': sort_order,
        'date_from': date_from,
        'date_to': date_to,
        'created_by_filter': created_by_filter,
        'users': users,
        'invoice_type': 'return_purchase',
        'invoice_type_name': 'فواتير مرتجع المشتريات',
    }
    
    return render(request, 'core/invoices/return_purchase.html', context)


@login_required
def invoices_return_sales_view(request):
    """
    View Return Sales invoices with filtering and sorting
    """
    # Get query parameters
    search = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'createdAt')
    sort_order = request.GET.get('sort_order', 'desc')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    created_by_filter = request.GET.get('created_by', '')
    
    # Build queryset for Return Sales invoices (type=4)
    queryset = InvoiceMaster.objects.filter(
        invoiceType=4,  # Return Sales invoices
        isDeleted=False
    ).select_related('customerOrVendorID', 'storeID', 'createdBy', 'originalInvoiceID')
    
    # Apply search filter
    if search:
        queryset = queryset.filter(
            Q(id__icontains=search) |
            Q(customerOrVendorID__customerVendorName__icontains=search) |
            Q(notes__icontains=search) |
            Q(originalInvoiceID__id__icontains=search)
        )
    
    # Apply date filters
    if date_from:
        queryset = queryset.filter(createdAt__date__gte=date_from)
    if date_to:
        queryset = queryset.filter(createdAt__date__lte=date_to)
    
    # Apply created by filter
    if created_by_filter:
        queryset = queryset.filter(
            Q(createdBy__id=created_by_filter) |
            Q(createdBy__username__icontains=created_by_filter)
        )
    
    # Apply sorting
    if sort_order == 'desc':
        sort_by = f'-{sort_by}'
    queryset = queryset.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all users for filter dropdown
    users = User.objects.filter(is_active=True).order_by('username')
    
    context = {
        'invoices': page_obj,
        'search': search,
        'sort_by': sort_by.lstrip('-'),
        'sort_order': sort_order,
        'date_from': date_from,
        'date_to': date_to,
        'created_by_filter': created_by_filter,
        'users': users,
        'invoice_type': 'return_sales',
        'invoice_type_name': 'فواتير مرتجع المبيعات',
    }
    
    return render(request, 'core/invoices/return_sales.html', context)


@login_required
def invoices_main_view(request):
    """
    Main invoices management page with navigation to 4 invoice types
    """
    # Get summary statistics for each invoice type
    purchase_count = InvoiceMaster.objects.filter(invoiceType=1, isDeleted=False).count()
    sales_count = InvoiceMaster.objects.filter(invoiceType=2, isDeleted=False).count()
    return_purchase_count = InvoiceMaster.objects.filter(invoiceType=3, isDeleted=False).count()
    return_sales_count = InvoiceMaster.objects.filter(invoiceType=4, isDeleted=False).count()
    
    context = {
        'purchase_count': purchase_count,
        'sales_count': sales_count,
        'return_purchase_count': return_purchase_count,
        'return_sales_count': return_sales_count,
    }
    
    return render(request, 'core/invoices/main.html', context)


@login_required
def invoice_detail_view(request, invoice_id):
    """
    Display detailed view of a specific invoice
    """
    try:
        # Get the invoice with all related data
        invoice = get_object_or_404(
            InvoiceMaster.objects.select_related(
                'customerOrVendorID', 'storeID', 'createdBy', 'agentID'
            ).prefetch_related('invoicedetail_set__item'),
            id=invoice_id, isDeleted=False
        )
        
        # Generate invoice number
        invoice_number = f'INV-{invoice.id:06d}'
        
        # Get invoice details (items)
        invoice_details = invoice.invoicedetail_set.all()
        
        # Calculate totals
        subtotal = sum(detail.quantity * detail.price for detail in invoice_details)
        
        # Determine invoice type label
        invoice_type_labels = {
            1: 'فاتورة شراء',
            2: 'فاتورة بيع', 
            3: 'مرتجع شراء',
            4: 'مرتجع بيع'
        }
        
        # Payment status based on actual status field and remaining amount
        if invoice.status == 0:
            payment_status = 'مدفوع'
        elif invoice.status == 1:
            payment_status = 'غير مدفوع'
        else:  # status == 2
            payment_status = 'مدفوع جزئياً'
            
        remaining_amount = invoice.netTotal - invoice.totalPaid
        
        # Calculate item totals for display
        invoice_details_with_totals = []
        for detail in invoice_details:
            detail_total = detail.quantity * detail.price
            invoice_details_with_totals.append({
                'detail': detail,
                'total': detail_total
            })
        
        # Get related object names safely
        customer_name = invoice.customerOrVendorID.customerVendorName if invoice.customerOrVendorID else 'غير محدد'
        store_name = invoice.storeID.storeName if invoice.storeID else 'غير محدد'
        agent_name = invoice.agentID.agentName if invoice.agentID else 'غير محدد'
        created_by_name = invoice.createdBy.username if invoice.createdBy else 'غير محدد'
        
        context = {
            'invoice': invoice,
            'invoice_number': invoice_number,
            'customer_name': customer_name,
            'store_name': store_name,
            'agent_name': agent_name,
            'created_by_name': created_by_name,
            'invoice_details': invoice_details,
            'invoice_details_with_totals': invoice_details_with_totals,
            'subtotal': subtotal,
            'remaining_amount': remaining_amount,
            'invoice_type_label': invoice_type_labels.get(invoice.invoiceType, 'غير محدد'),
            'payment_status': payment_status,
        }
        
        return render(request, 'core/invoices/detail.html', context)
        
    except Exception as e:
        messages.error(request, f'حدث خطأ في تحميل تفاصيل الفاتورة: {str(e)}')
        return redirect('core:invoices_main')


# Customer/Vendor Management Views


@login_required
def customer_add_view(request):
    """
    Add a new customer
    """
    if request.method == 'POST':
        customer_name = request.POST.get('customerVendorName', '').strip()
        phone_one = request.POST.get('phone_one', '').strip()
        phone_two = request.POST.get('phone_two', '').strip()
        notes = request.POST.get('notes', '').strip()
        pricelist_id = request.POST.get('pricelist_id')
        
        if not customer_name:
            messages.error(request, 'اسم العميل مطلوب')
            return redirect('core:customer_add')
        
        try:
            # Create customer (type=1 for customer)
            customer = CustomerVendor.objects.create(
                customerVendorName=customer_name,
                phone_one=phone_one or None,
                phone_two=phone_two or None,
                type=1,  # Customer
                notes=notes or None,
                createdBy=request.user
            )
            
            # Bind to price list if selected
            if pricelist_id:
                try:
                    pricelist = PriceList.objects.get(id=pricelist_id, isDeleted=False)
                    CustomerVendorPriceList.objects.create(
                        customerVendorID=customer,
                        priceListID=pricelist,
                        createdBy=request.user
                    )
                except (PriceList.DoesNotExist, ValueError):
                    pass  # Ignore if pricelist doesn't exist
            
            messages.success(request, f'تم إنشاء العميل "{customer_name}" بنجاح')
            return redirect('core:customers')
            
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء إنشاء العميل: {str(e)}')
    
    # Get available price lists for dropdown
    pricelists = PriceList.objects.filter(isDeleted=False).order_by('priceListName')
    
    context = {
        'pricelists': pricelists,
    }
    
    return render(request, 'core/customers/add.html', context)


@login_required
def vendor_add_view(request):
    """
    Add a new vendor
    """
    if request.method == 'POST':
        vendor_name = request.POST.get('customerVendorName', '').strip()
        phone_one = request.POST.get('phone_one', '').strip()
        phone_two = request.POST.get('phone_two', '').strip()
        notes = request.POST.get('notes', '').strip()
        pricelist_id = request.POST.get('pricelist_id')
        
        if not vendor_name:
            messages.error(request, 'اسم المورد مطلوب')
            return redirect('core:vendor_add')
        
        try:
            # Create vendor (type=2 for vendor)
            vendor = CustomerVendor.objects.create(
                customerVendorName=vendor_name,
                phone_one=phone_one or None,
                phone_two=phone_two or None,
                type=2,  # Vendor
                notes=notes or None,
                createdBy=request.user
            )
            
            # Bind to price list if selected
            if pricelist_id:
                try:
                    pricelist = PriceList.objects.get(id=pricelist_id, isDeleted=False)
                    CustomerVendorPriceList.objects.create(
                        customerVendorID=vendor,
                        priceListID=pricelist,
                        createdBy=request.user
                    )
                except (PriceList.DoesNotExist, ValueError):
                    pass  # Ignore if pricelist doesn't exist
            
            messages.success(request, f'تم إنشاء المورد "{vendor_name}" بنجاح')
            return redirect('core:vendors')
            
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء إنشاء المورد: {str(e)}')
    
    # Get available price lists for dropdown
    pricelists = PriceList.objects.filter(isDeleted=False).order_by('priceListName')
    
    context = {
        'pricelists': pricelists,
    }
    
    return render(request, 'core/vendors/add.html', context)


@login_required
def customer_edit_view(request, customer_id):
    """
    Edit an existing customer
    """
    customer = get_object_or_404(CustomerVendor, id=customer_id, isDeleted=False, type__in=[1, 3])
    
    if request.method == 'POST':
        customer_name = request.POST.get('customerVendorName', '').strip()
        phone_one = request.POST.get('phone_one', '').strip()
        phone_two = request.POST.get('phone_two', '').strip()
        notes = request.POST.get('notes', '').strip()
        pricelist_id = request.POST.get('pricelist_id')
        
        if not customer_name:
            messages.error(request, 'اسم العميل مطلوب')
            return redirect('core:customer_edit', customer_id=customer_id)
        
        try:
            # Update customer
            customer.customerVendorName = customer_name
            customer.phone_one = phone_one or None
            customer.phone_two = phone_two or None
            customer.notes = notes or None
            customer.updatedBy = request.user
            customer.save()
            
            # Update price list binding
            CustomerVendorPriceList.objects.filter(customerVendorID=customer).delete()
            if pricelist_id:
                try:
                    pricelist = PriceList.objects.get(id=pricelist_id, isDeleted=False)
                    CustomerVendorPriceList.objects.create(
                        customerVendorID=customer,
                        priceListID=pricelist,
                        createdBy=request.user
                    )
                except (PriceList.DoesNotExist, ValueError):
                    pass  # Ignore if pricelist doesn't exist
            
            messages.success(request, f'تم تحديث العميل "{customer_name}" بنجاح')
            return redirect('core:customers')
            
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء تحديث العميل: {str(e)}')
    
    # Get available price lists for dropdown
    pricelists = PriceList.objects.filter(isDeleted=False).order_by('priceListName')
    
    # Get current price list binding
    current_pricelist = None
    try:
        pricelist_binding = CustomerVendorPriceList.objects.get(customerVendorID=customer)
        current_pricelist = pricelist_binding.priceListID
    except CustomerVendorPriceList.DoesNotExist:
        pass
    
    context = {
        'customer': customer,
        'pricelists': pricelists,
        'current_pricelist': current_pricelist,
    }
    
    return render(request, 'core/customers/edit.html', context)


@login_required
def vendor_edit_view(request, vendor_id):
    """
    Edit an existing vendor
    """
    vendor = get_object_or_404(CustomerVendor, id=vendor_id, isDeleted=False, type__in=[2, 3])
    
    if request.method == 'POST':
        vendor_name = request.POST.get('customerVendorName', '').strip()
        phone_one = request.POST.get('phone_one', '').strip()
        phone_two = request.POST.get('phone_two', '').strip()
        notes = request.POST.get('notes', '').strip()
        pricelist_id = request.POST.get('pricelist_id')
        
        if not vendor_name:
            messages.error(request, 'اسم المورد مطلوب')
            return redirect('core:vendor_edit', vendor_id=vendor_id)
        
        try:
            # Update vendor
            vendor.customerVendorName = vendor_name
            vendor.phone_one = phone_one or None
            vendor.phone_two = phone_two or None
            vendor.notes = notes or None
            vendor.updatedBy = request.user
            vendor.save()
            
            # Update price list binding
            CustomerVendorPriceList.objects.filter(customerVendorID=vendor).delete()
            if pricelist_id:
                try:
                    pricelist = PriceList.objects.get(id=pricelist_id, isDeleted=False)
                    CustomerVendorPriceList.objects.create(
                        customerVendorID=vendor,
                        priceListID=pricelist,
                        createdBy=request.user
                    )
                except (PriceList.DoesNotExist, ValueError):
                    pass  # Ignore if pricelist doesn't exist
            
            messages.success(request, f'تم تحديث المورد "{vendor_name}" بنجاح')
            return redirect('core:vendors')
            
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء تحديث المورد: {str(e)}')
    
    # Get available price lists for dropdown
    pricelists = PriceList.objects.filter(isDeleted=False).order_by('priceListName')
    
    # Get current price list binding
    current_pricelist = None
    try:
        pricelist_binding = CustomerVendorPriceList.objects.get(customerVendorID=vendor)
        current_pricelist = pricelist_binding.priceListID
    except CustomerVendorPriceList.DoesNotExist:
        pass
    
    context = {
        'vendor': vendor,
        'pricelists': pricelists,
        'current_pricelist': current_pricelist,
    }
    
    return render(request, 'core/vendors/edit.html', context)


@login_required
def customer_delete_view(request, customer_id):
    """
    Delete a customer (soft delete)
    """
    customer = get_object_or_404(CustomerVendor, id=customer_id, isDeleted=False, type__in=[1, 3])
    
    # Check if customer is referenced in invoices
    if InvoiceMaster.objects.filter(customerOrVendorID=customer, isDeleted=False).exists():
        messages.error(request, 'لا يمكن حذف العميل لأنه مرتبط بفواتير')
        return redirect('core:customers')
    
    if request.method == 'POST':
        try:
            customer.isDeleted = True
            customer.deletedBy = request.user
            customer.deletedAt = timezone.now()
            customer.updatedBy = request.user
            customer.save()
            
            # Also delete price list bindings
            CustomerVendorPriceList.objects.filter(customerVendorID=customer).delete()
            
            messages.success(request, f'تم حذف العميل "{customer.customerVendorName}" بنجاح')
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف العميل: {str(e)}')
        
        return redirect('core:customers')
    
    context = {
        'customer': customer,
    }
    
    return render(request, 'core/customers/delete.html', context)


@login_required
def vendor_delete_view(request, vendor_id):
    """
    Delete a vendor (soft delete)
    """
    vendor = get_object_or_404(CustomerVendor, id=vendor_id, isDeleted=False, type__in=[2, 3])
    
    # Check if vendor is referenced in invoices
    if InvoiceMaster.objects.filter(customerOrVendorID=vendor, isDeleted=False).exists():
        messages.error(request, 'لا يمكن حذف المورد لأنه مرتبط بفواتير')
        return redirect('core:vendors')
    
    if request.method == 'POST':
        try:
            vendor.isDeleted = True
            vendor.deletedBy = request.user
            vendor.deletedAt = timezone.now()
            vendor.updatedBy = request.user
            vendor.save()
            
            # Also delete price list bindings
            CustomerVendorPriceList.objects.filter(customerVendorID=vendor).delete()
            
            messages.success(request, f'تم حذف المورد "{vendor.customerVendorName}" بنجاح')
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف المورد: {str(e)}')
        
        return redirect('core:vendors')
    
    context = {
        'vendor': vendor,
    }
    
    return render(request, 'core/vendors/delete.html', context)


# Agent API Views
@extend_schema(
    summary="List all agents",
    description="Retrieve a list of all agents with filtering options",
    parameters=[
        OpenApiParameter(name='agent_name', type=OpenApiTypes.STR, description='Filter by agent name'),
        OpenApiParameter(name='username', type=OpenApiTypes.STR, description='Filter by username'),
        OpenApiParameter(name='search', type=OpenApiTypes.STR, description='Search in agent name and username')
    ]
)
@api_view(['GET'])
def agent_list(request):
    """Get all agents with optional filtering"""
    try:
        queryset = Agent.objects.filter(isDeleted=False)
        
        # Apply filters
        agent_name = request.GET.get('agent_name', None)
        username = request.GET.get('username', None)
        search = request.GET.get('search', None)
        
        if agent_name:
            queryset = queryset.filter(agentName__icontains=agent_name)
        
        if username:
            queryset = queryset.filter(agentUserID__username__icontains=username)
        
        if search:
            queryset = queryset.filter(
                Q(agentName__icontains=search) |
                Q(agentUserID__username__icontains=search) |
                Q(agentUserID__first_name__icontains=search) |
                Q(agentUserID__last_name__icontains=search)
            )
        
        serializer = AgentSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Create a new agent",
    description="Create a new agent",
    request=AgentSerializer
)
@api_view(['POST'])
def agent_create(request):
    """Create a new agent"""
    try:
        serializer = AgentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Set the createdBy field to the current user or first admin user
            created_by_user = None
            if hasattr(request, 'user') and request.user.is_authenticated:
                created_by_user = request.user
            else:
                # For API calls without authentication, use the first admin user
                from django.contrib.auth.models import User
                created_by_user = User.objects.filter(is_superuser=True).first()
                if not created_by_user:
                    created_by_user = User.objects.first()
            
            agent = serializer.save(createdBy=created_by_user, updatedBy=created_by_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Get agent by ID",
    description="Retrieve a specific agent by ID",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Agent ID')
    ]
)
@api_view(['GET'])
def agent_detail(request, id):
    """Get specific agent by ID"""
    try:
        agent = get_object_or_404(Agent, id=id, isDeleted=False)
        serializer = AgentSerializer(agent, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Update agent by ID",
    description="Update a specific agent by ID",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Agent ID')
    ],
    request=AgentSerializer
)
@api_view(['PUT'])
def agent_update(request, id):
    """Update specific agent by ID"""
    try:
        agent = get_object_or_404(Agent, id=id, isDeleted=False)
        serializer = AgentSerializer(agent, data=request.data, context={'request': request})
        if serializer.is_valid():
            # Set the updatedBy field to the current user
            serializer.save(updatedBy=request.user if hasattr(request, 'user') and request.user.is_authenticated else None)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Delete agent by ID",
    description="Soft delete a specific agent by ID",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='Agent ID')
    ]
)
@api_view(['DELETE'])
def agent_delete(request, id):
    """Soft delete specific agent by ID"""
    try:
        agent = get_object_or_404(Agent, id=id, isDeleted=False)
        
        # Perform soft delete
        agent.isDeleted = True
        agent.deletedBy = request.user if hasattr(request, 'user') and request.user.is_authenticated else None
        agent.deletedAt = timezone.now()
        agent.save()
        
        return Response({'message': 'Agent deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== AGENT AUTHENTICATION VIEWS ====================

@extend_schema(
    summary="Agent login",
    description="Authenticate agent using username and password for mobile app access",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'description': 'Agent username'},
                'password': {'type': 'string', 'description': 'Agent password'},
            },
            'required': ['username', 'password']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'message': {'type': 'string'},
                'agent': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'agentName': {'type': 'string'},
                        'agentUsername': {'type': 'string'},
                        'agentPhone': {'type': 'string'},
                        'isActive': {'type': 'boolean'},
                    }
                },
                'token': {'type': 'string', 'description': 'Simple session token (agent ID)'}
            }
        },
        400: {'description': 'Invalid credentials or inactive agent'},
        401: {'description': 'Authentication failed'}
    }
)
@api_view(['POST'])
def agent_login(request):
    """
    Agent login endpoint for mobile app authentication.
    Returns agent data and simple token for session management.
    """
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'success': False,
                'message': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Find agent by username
        try:
            agent = Agent.objects.get(
                agentUsername=username, 
                isDeleted=False
            )
        except Agent.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check password
        if not agent.check_password(password):
            return Response({
                'success': False,
                'message': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if agent is active
        if not agent.isActive:
            return Response({
                'success': False,
                'message': 'Agent account is inactive'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Return success response with agent data
        return Response({
            'success': True,
            'message': 'Login successful',
            'agent': {
                'id': agent.id,
                'agentName': agent.agentName,
                'agentUsername': agent.agentUsername,
                'agentPhone': agent.agentPhone,
                'isActive': agent.isActive,
            },
            'token': str(agent.id)  # Simple token for mobile app sessions
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Login failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Agent logout",
    description="Logout agent (for session cleanup on mobile app)",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'token': {'type': 'string', 'description': 'Agent session token'},
            },
            'required': ['token']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'message': {'type': 'string'},
            }
        }
    }
)
@api_view(['POST'])
def agent_logout(request):
    """
    Agent logout endpoint for mobile app session cleanup.
    Simple implementation since we're using stateless authentication.
    """
    try:
        token = request.data.get('token')
        
        if not token:
            return Response({
                'success': False,
                'message': 'Token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # For stateless authentication, we just return success
        # Mobile app should clear local storage/session data
        return Response({
            'success': True,
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Logout failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Verify agent token",
    description="Verify agent session token and return agent information",
    parameters=[
        OpenApiParameter(name='token', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description='Agent session token')
    ],
    responses={
        200: {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'agent': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'agentName': {'type': 'string'},
                        'agentUsername': {'type': 'string'},
                        'agentPhone': {'type': 'string'},
                        'isActive': {'type': 'boolean'},
                    }
                }
            }
        },
        401: {'description': 'Invalid or expired token'}
    }
)
@api_view(['GET'])
def agent_verify_token(request):
    """
    Verify agent token and return agent information.
    Used by mobile app to validate session and get agent data.
    """
    try:
        token = request.GET.get('token')
        
        if not token:
            return Response({
                'success': False,
                'message': 'Token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Try to get agent by ID (token is agent ID)
        try:
            agent_id = int(token)
            agent = Agent.objects.get(
                id=agent_id,
                isDeleted=False,
                isActive=True
            )
        except (ValueError, Agent.DoesNotExist):
            return Response({
                'success': False,
                'message': 'Invalid token'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Return agent information
        return Response({
            'success': True,
            'agent': {
                'id': agent.id,
                'agentName': agent.agentName,
                'agentUsername': agent.agentUsername,
                'agentPhone': agent.agentPhone,
                'isActive': agent.isActive,
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Token verification failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =============================================================================
# VOUCHER API ENDPOINTS
# =============================================================================

from functools import wraps
from django.contrib.auth.hashers import check_password
import base64
from datetime import datetime

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


def generate_voucher_id(agent_id, voucher_type):
    """
    Generate voucher ID in format: {agent_id}000{r|p}{auto_increment}
    Examples: 2000r001, 2000p003
    """
    from django.db import connection
    
    # Determine type suffix
    type_suffix = 'r' if voucher_type == 1 else 'p'
    prefix = f"{agent_id}000{type_suffix}"
    
    # Get next sequence number for this agent and type
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) + 1 
            FROM transactions 
            WHERE notes LIKE %s
        """, [f"{prefix}%"])
        sequence = cursor.fetchone()[0]
    
    return f"{prefix}{sequence:03d}"


@extend_schema(
    summary="Create a new voucher",
    description="""
    Create a new voucher (receipt or payment) by an agent.
    
    **Authentication Required**: Basic Auth with agent credentials
    
    **Voucher Types**:
    - type=1: Receipt (money IN from customers)
    - type=2: Payment (money OUT to vendors)
    
    **Processing**:
    - Creates 2 accounting transactions (debit/credit)
    - Generates unique voucher ID
    - Updates customer/vendor balances
    """,
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'voucherType': {'type': 'string', 'enum': ['receipt', 'payment']},
                'type': {'type': 'integer', 'enum': [1, 2]},
                'customerVendorId': {'type': 'integer'},
                'amount': {'type': 'number', 'format': 'decimal'},
                'paymentMethod': {'type': 'string', 'default': 'cash'},
                'accountId': {'type': 'integer', 'default': 35},
                'notes': {'type': 'string'},
                'voucherDate': {'type': 'string', 'format': 'date-time'},
                'storeId': {'type': 'integer'}
            },
            'required': ['type', 'customerVendorId', 'amount', 'storeId']
        }
    },
    responses={
        201: {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'voucherId': {'type': 'string'},
                'transactionIds': {'type': 'array', 'items': {'type': 'integer'}},
                'message': {'type': 'string'}
            }
        }
    }
)
@api_view(['POST'])
@agent_authentication_required
def create_voucher(request):
    """
    Create a new voucher with double-entry accounting
    """
    try:
        # Extract request data
        data = request.data
        voucher_type = data.get('type')
        customer_vendor_id = data.get('customerVendorId')
        amount = Decimal(str(data.get('amount', 0)))
        payment_method = data.get('paymentMethod', 'cash')
        account_id = data.get('accountId', 35)  # Default to cash account
        notes = data.get('notes', '')
        voucher_date = data.get('voucherDate')
        store_id = data.get('storeId')
        
        # Validation
        if not voucher_type or voucher_type not in [1, 2]:
            return Response({
                'success': False,
                'error': 'INVALID_TYPE',
                'message': 'Type must be 1 (receipt) or 2 (payment)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not customer_vendor_id or not amount or not store_id:
            return Response({
                'success': False,
                'error': 'MISSING_REQUIRED_FIELDS',
                'message': 'customerVendorId, amount, and storeId are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if amount <= 0:
            return Response({
                'success': False,
                'error': 'INVALID_AMOUNT',
                'message': 'Amount must be greater than 0'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify customer/vendor exists
        try:
            customer_vendor = CustomerVendor.objects.get(id=customer_vendor_id, isDeleted=False)
        except CustomerVendor.DoesNotExist:
            return Response({
                'success': False,
                'error': 'CUSTOMER_VENDOR_NOT_FOUND',
                'message': f'Customer/Vendor with ID {customer_vendor_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Verify store exists
        try:
            store = Store.objects.get(id=store_id, isDeleted=False)
        except Store.DoesNotExist:
            return Response({
                'success': False,
                'error': 'STORE_NOT_FOUND',
                'message': f'Store with ID {store_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Verify cash account exists
        try:
            cash_account = Account.objects.get(id=account_id, isDeleted=False)
        except Account.DoesNotExist:
            return Response({
                'success': False,
                'error': 'ACCOUNT_NOT_FOUND',
                'message': f'Account with ID {account_id} not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Generate voucher ID
        voucher_id = generate_voucher_id(request.agent.id, voucher_type)
        
        # Parse voucher date
        if voucher_date:
            try:
                voucher_datetime = datetime.fromisoformat(voucher_date.replace('Z', '+00:00'))
            except:
                voucher_datetime = timezone.now()
        else:
            voucher_datetime = timezone.now()
        
        # Create transactions based on voucher type
        transaction_ids = []
        
        if voucher_type == 1:  # Receipt (Money IN)
            # Transaction 1: Debit Cash Account (Money IN)
            transaction1 = Transaction.objects.create(
                accountID=cash_account,
                amount=amount,  # Positive (Debit)
                notes=f"Cash received - Voucher {voucher_id} - {customer_vendor.customerName}",
                type=voucher_type,
                customerVendorID=None,  # No customer/vendor for cash account
                createdBy=request.agent.createdBy,  # Use agent's creator as proxy
                createdAt=voucher_datetime
            )
            transaction_ids.append(transaction1.id)
            
            # Transaction 2: Credit Customer Account (Reduce customer debt)
            transaction2 = Transaction.objects.create(
                accountID=Account.objects.get(id=36),  # Customer AR account
                amount=-amount,  # Negative (Credit)
                notes=f"Payment received - Voucher {voucher_id} - Agent {request.agent.agentName}",
                type=voucher_type,
                customerVendorID=customer_vendor,
                createdBy=request.agent.createdBy,
                createdAt=voucher_datetime
            )
            transaction_ids.append(transaction2.id)
            
        else:  # Payment (Money OUT)
            # Transaction 1: Debit Vendor Account (Reduce business debt)
            transaction1 = Transaction.objects.create(
                accountID=Account.objects.get(id=37),  # Vendor AP account
                amount=amount,  # Positive (Debit)
                notes=f"Payment made - Voucher {voucher_id} - Agent {request.agent.agentName}",
                type=voucher_type,
                customerVendorID=customer_vendor,
                createdBy=request.agent.createdBy,
                createdAt=voucher_datetime
            )
            transaction_ids.append(transaction1.id)
            
            # Transaction 2: Credit Cash Account (Money OUT)
            transaction2 = Transaction.objects.create(
                accountID=cash_account,
                amount=-amount,  # Negative (Credit)
                notes=f"Cash payment - Voucher {voucher_id} - {customer_vendor.customerName}",
                type=voucher_type,
                customerVendorID=None,
                createdBy=request.agent.createdBy,
                createdAt=voucher_datetime
            )
            transaction_ids.append(transaction2.id)
        
        return Response({
            'success': True,
            'voucherId': voucher_id,
            'transactionIds': transaction_ids,
            'message': f'Voucher {voucher_id} created successfully',
            'amount': float(amount),
            'customerVendor': customer_vendor.customerName,
            'agent': request.agent.agentName
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': 'PROCESSING_ERROR',
            'message': f'Error creating voucher: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Get vouchers with filters",
    description="""
    Retrieve vouchers (transactions) created by agents with optional filters.
    
    **Authentication Required**: Basic Auth with agent credentials
    
    **Filters**:
    - agent_id: Filter by specific agent (optional)
    - date_from: Start date filter (YYYY-MM-DD)
    - date_to: End date filter (YYYY-MM-DD)
    - type: Transaction type (1=receipt, 2=payment)
    """,
    parameters=[
        OpenApiParameter('agent_id', OpenApiTypes.INT, description='Filter by agent ID'),
        OpenApiParameter('date_from', OpenApiTypes.DATE, description='Start date (YYYY-MM-DD)'),
        OpenApiParameter('date_to', OpenApiTypes.DATE, description='End date (YYYY-MM-DD)'),
        OpenApiParameter('type', OpenApiTypes.INT, description='Voucher type (1=receipt, 2=payment)'),
        OpenApiParameter('page', OpenApiTypes.INT, description='Page number'),
        OpenApiParameter('page_size', OpenApiTypes.INT, description='Items per page (max 100)'),
    ],
    responses={
        200: {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'count': {'type': 'integer'},
                'next': {'type': 'string'},
                'previous': {'type': 'string'},
                'results': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'voucherId': {'type': 'string'},
                            'amount': {'type': 'number'},
                            'type': {'type': 'integer'},
                            'customerVendor': {'type': 'string'},
                            'notes': {'type': 'string'},
                            'createdAt': {'type': 'string', 'format': 'date-time'}
                        }
                    }
                }
            }
        }
    }
)
@api_view(['GET'])
@agent_authentication_required
def get_vouchers(request):
    """
    Get vouchers with filtering capabilities
    """
    try:
        # Get query parameters
        agent_id = request.GET.get('agent_id')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        voucher_type = request.GET.get('type')
        page = int(request.GET.get('page', 1))
        page_size = min(int(request.GET.get('page_size', 20)), 100)
        
        # Build query for voucher transactions
        # Look for transactions that contain voucher IDs in notes
        query = Q(notes__icontains='Voucher')
        
        # Filter by agent if specified
        if agent_id:
            query &= Q(notes__icontains=f"{agent_id}000")
        
        # Filter by date range
        if date_from:
            try:
                date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d').date()
                query &= Q(createdAt__date__gte=date_from_parsed)
            except ValueError:
                return Response({
                    'success': False,
                    'error': 'INVALID_DATE_FORMAT',
                    'message': 'date_from must be in YYYY-MM-DD format'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        if date_to:
            try:
                date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d').date()
                query &= Q(createdAt__date__lte=date_to_parsed)
            except ValueError:
                return Response({
                    'success': False,
                    'error': 'INVALID_DATE_FORMAT',
                    'message': 'date_to must be in YYYY-MM-DD format'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter by voucher type
        if voucher_type:
            try:
                voucher_type_int = int(voucher_type)
                if voucher_type_int in [1, 2]:
                    query &= Q(type=voucher_type_int)
            except ValueError:
                pass
        
        # Get transactions
        transactions = Transaction.objects.filter(
            query,
            isDeleted=False
        ).select_related('accountID', 'customerVendorID').order_by('-createdAt')
        
        # Group transactions by voucher ID (extract from notes)
        vouchers = {}
        for transaction in transactions:
            # Extract voucher ID from notes
            notes = transaction.notes or ''
            voucher_id = None
            if 'Voucher ' in notes:
                try:
                    voucher_start = notes.find('Voucher ') + 8
                    voucher_end = notes.find(' ', voucher_start)
                    if voucher_end == -1:
                        voucher_end = notes.find('-', voucher_start)
                    if voucher_end == -1:
                        voucher_end = len(notes)
                    voucher_id = notes[voucher_start:voucher_end].strip()
                except:
                    continue
            
            if voucher_id and voucher_id not in vouchers:
                # Only include cash transactions (positive amounts for receipts, negative for payments)
                if ((transaction.type == 1 and transaction.amount > 0) or 
                    (transaction.type == 2 and transaction.amount < 0)):
                    vouchers[voucher_id] = {
                        'voucherId': voucher_id,
                        'amount': abs(float(transaction.amount)),
                        'type': transaction.type,
                        'customerVendor': transaction.customerVendorID.customerName if transaction.customerVendorID else 'N/A',
                        'notes': transaction.notes,
                        'createdAt': transaction.createdAt.isoformat(),
                        'accountName': transaction.accountID.accountName if transaction.accountID else 'N/A'
                    }
        
        # Convert to list and paginate
        voucher_list = list(vouchers.values())
        
        # Manual pagination
        total_count = len(voucher_list)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_vouchers = voucher_list[start_index:end_index]
        
        # Build pagination URLs
        base_url = request.build_absolute_uri().split('?')[0]
        next_url = None
        previous_url = None
        
        if end_index < total_count:
            next_params = request.GET.copy()
            next_params['page'] = page + 1
            next_url = f"{base_url}?{next_params.urlencode()}"
        
        if page > 1:
            prev_params = request.GET.copy()
            prev_params['page'] = page - 1
            previous_url = f"{base_url}?{prev_params.urlencode()}"
        
        return Response({
            'success': True,
            'count': total_count,
            'next': next_url,
            'previous': previous_url,
            'results': paginated_vouchers,
            'page': page,
            'page_size': page_size,
            'total_pages': (total_count + page_size - 1) // page_size
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': 'PROCESSING_ERROR',
            'message': f'Error retrieving vouchers: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
