from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.utils import timezone
from core.models import ItemsGroup, Item, PriceList, Store, StoreGroup, CustomerVendor, InvoiceMaster
from .forms import CustomUserCreationForm, CustomUserEditForm

# API imports
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import json
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny


@never_cache
@csrf_protect
def login_view(request):
    """
    Handle user login with authentication
    """
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'مرحباً بعودتك، {user.get_full_name() or user.username}!')
                    
                    # Redirect to next page if specified, otherwise to dashboard
                    next_page = request.GET.get('next', 'authentication:dashboard')
                    return redirect(next_page)
                else:
                    messages.error(request, 'حسابك معطل. يرجى التواصل مع الإدارة.')
            else:
                messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة. يرجى المحاولة مرة أخرى.')
        else:
            messages.error(request, 'يرجى إدخال اسم المستخدم وكلمة المرور.')
    
    context = {
        'form': {'username': {'value': request.POST.get('username', '')}} if request.method == 'POST' else {},
    }
    return render(request, 'authentication/login.html', context)


@login_required
def logout_view(request):
    """
    Handle user logout
    """
    username = request.user.username
    logout(request)
    messages.success(request, f'وداعاً {username}! تم تسجيل خروجك بنجاح.')
    return redirect('authentication:login')


@login_required
def dashboard_view(request):
    """
    Dashboard page showing system overview
    Requires user authentication
    """
    # Get statistics for dashboard
    try:
        items_groups_count = ItemsGroup.objects.filter(isDeleted=False).count()
        items_count = Item.objects.filter(isDeleted=False).count()
        price_lists_count = PriceList.objects.filter(isDeleted=False).count()
        store_groups_count = StoreGroup.objects.filter(isDeleted=False).count()
        stores_count = Store.objects.filter(isDeleted=False).count()
        
        # Customer and vendor counts
        customers_count = CustomerVendor.objects.filter(isDeleted=False, type__in=[1, 3]).count()
        vendors_count = CustomerVendor.objects.filter(isDeleted=False, type__in=[2, 3]).count()
        
        # Invoice counts by type
        from core.models import InvoiceMaster
        purchase_invoices_count = InvoiceMaster.objects.filter(isDeleted=False, invoiceType=1).count()
        sales_invoices_count = InvoiceMaster.objects.filter(isDeleted=False, invoiceType=2).count()
        return_purchase_invoices_count = InvoiceMaster.objects.filter(isDeleted=False, invoiceType=3).count()
        return_sales_invoices_count = InvoiceMaster.objects.filter(isDeleted=False, invoiceType=4).count()
        total_invoices_count = InvoiceMaster.objects.filter(isDeleted=False).count()
        
    except Exception as e:
        # In case of database issues, set counts to 0
        items_groups_count = items_count = price_lists_count = store_groups_count = stores_count = 0
        customers_count = vendors_count = 0
        purchase_invoices_count = sales_invoices_count = return_purchase_invoices_count = return_sales_invoices_count = total_invoices_count = 0
        messages.warning(request, 'لا يمكن تحميل الإحصائيات. يرجى التحقق من اتصال قاعدة البيانات.')
    
    # Get user's groups for permission checking
    user = request.user
    user_groups = list(user.groups.values_list('name', flat=True))
    is_superuser = user.is_superuser
    
    # Check for specific groups
    # Available groups: إدارة, أمناء مخازن, مدخلوا بيانات, مناديب
    is_admin = 'إدارة' in user_groups
    is_store_keeper = 'أمناء مخازن' in user_groups
    is_data_entry = 'مدخلوا بيانات' in user_groups
    is_agent = 'مناديب' in user_groups
    
    # Card visibility dictionary - controls which dashboard cards each user group can see
    # Superusers and إدارة can see all cards
    # أمناء مخازن can ONLY see إدارة المخزون
    card_visibility = {
        # Statistics Row 1
        'items_groups': is_superuser or is_admin or (not is_store_keeper and True),      # مجموعات الأصناف
        'items': is_superuser or is_admin or (not is_store_keeper and True),              # الأصناف
        'customers': is_superuser or is_admin or (not is_store_keeper and True),          # العملاء
        'vendors': is_superuser or is_admin or (not is_store_keeper and True),            # الموردين
        
        # Statistics Row 2
        'price_lists': is_superuser or is_admin or (not is_store_keeper and True),        # قوائم الأسعار
        'store_groups': is_superuser or is_admin or (not is_store_keeper and True),       # مجموعات المخازن
        'stores': is_superuser or is_admin or (not is_store_keeper and True),             # المخازن
        'invoices': is_superuser or is_admin or (not is_store_keeper and True),           # إجمالي الفواتير
        
        # Management Row
        'agents_manage': is_superuser or is_admin or (not is_store_keeper and True),      # إدارة المناديب
        'visit_plans': is_superuser or is_admin or (not is_store_keeper and True),        # خطط الزيارات
        'inventory': is_superuser or is_admin or is_store_keeper,                          # إدارة المخزون
        'users_manage': is_superuser or is_admin or (not is_store_keeper and True),       # إدارة المستخدمين
    }
    
    context = {
        'items_groups_count': items_groups_count,
        'items_count': items_count,
        'price_lists_count': price_lists_count,
        'store_groups_count': store_groups_count,
        'stores_count': stores_count,
        'customers_count': customers_count,
        'vendors_count': vendors_count,
        'purchase_invoices_count': purchase_invoices_count,
        'sales_invoices_count': sales_invoices_count,
        'return_purchase_invoices_count': return_purchase_invoices_count,
        'return_sales_invoices_count': return_sales_invoices_count,
        'total_invoices_count': total_invoices_count,
        'user': request.user,
        'card_visibility': card_visibility,
        'user_groups': user_groups,
    }
    
    return render(request, 'authentication/dashboard.html', context)


def index_view(request):
    """
    Index page - redirects to login if not authenticated, dashboard if authenticated
    """
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    else:
        return redirect('authentication:login')


# User Management Views

@login_required
def users_list_view(request):
    """
    Display list of all users with search and pagination
    """
    # Check if user has permission to view users
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'ليس لديك صلاحية لعرض المستخدمين')
        return redirect('authentication:dashboard')
    
    # Get search query
    search_query = request.GET.get('search', '').strip()
    
    # Start with all users excluding superusers
    users_queryset = User.objects.filter(is_superuser=False)
    
    # Apply search filter
    if search_query:
        users_queryset = users_queryset.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Apply ordering
    users_queryset = users_queryset.order_by('-date_joined')
    
    # Apply pagination
    paginator = Paginator(users_queryset, 20)  # Show 20 users per page
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    context = {
        'users': users,
        'search_query': search_query,
        'total_users': User.objects.filter(is_superuser=False).count(),
    }
    
    return render(request, 'authentication/users/list.html', context)


@login_required
def user_create_view(request):
    """
    Create a new user with custom form that allows spaces in usernames
    """
    # Check if user has permission to create users
    if not request.user.is_superuser:
        messages.error(request, 'ليس لديك صلاحية لإنشاء مستخدمين جدد')
        return redirect('authentication:users_list')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                # Create user
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email='',  # Set email to empty string by default
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )
                user.is_staff = form.cleaned_data['is_staff']
                user.is_active = form.cleaned_data['is_active']
                user.save()
                
                messages.success(request, f'تم إنشاء المستخدم "{user.username}" بنجاح')
                return redirect('authentication:users_list')
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء إنشاء المستخدم: {str(e)}')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'authentication/users/create.html', {'form': form})


@login_required
def user_edit_view(request, user_id):
    """
    Edit an existing user with custom form that allows spaces in usernames
    """
    # Check if user has permission to edit users
    if not request.user.is_superuser:
        messages.error(request, 'ليس لديك صلاحية لتعديل المستخدمين')
        return redirect('authentication:users_list')
    
    user_to_edit = get_object_or_404(User, id=user_id)
    
    # Prevent editing superuser accounts
    if user_to_edit.is_superuser:
        messages.error(request, 'لا يمكن تعديل حسابات المدير العام. يرجى استخدام لوحة الإدارة أو الطرفية')
        return redirect('authentication:users_list')
    
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            try:
                # Update user
                user_to_edit.username = form.cleaned_data['username']
                # Keep existing email or set to empty string if None
                if not user_to_edit.email:
                    user_to_edit.email = ''
                user_to_edit.first_name = form.cleaned_data['first_name']
                user_to_edit.last_name = form.cleaned_data['last_name']
                user_to_edit.is_staff = form.cleaned_data['is_staff']
                user_to_edit.is_active = form.cleaned_data['is_active']
                
                # Update password if provided
                password = form.cleaned_data.get('password')
                if password:
                    user_to_edit.set_password(password)
                
                user_to_edit.save()
                
                messages.success(request, f'تم تحديث المستخدم "{user_to_edit.username}" بنجاح')
                return redirect('authentication:users_list')
                
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء تحديث المستخدم: {str(e)}')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomUserEditForm(instance=user_to_edit)
    
    context = {
        'user_to_edit': user_to_edit,
        'form': form,
    }
    
    return render(request, 'authentication/users/edit.html', context)


@login_required
def user_delete_view(request, user_id):
    """
    Delete a user (soft delete by deactivating)
    """
    # Check if user has permission to delete users
    if not request.user.is_superuser:
        messages.error(request, 'ليس لديك صلاحية لحذف المستخدمين')
        return redirect('authentication:users_list')
    
    user_to_delete = get_object_or_404(User, id=user_id)
    
    # Prevent deleting superuser accounts
    if user_to_delete.is_superuser:
        messages.error(request, 'لا يمكن حذف حسابات المدير العام. يرجى استخدام لوحة الإدارة أو الطرفية')
        return redirect('authentication:users_list')
    
    # Prevent deleting self
    if user_to_delete == request.user:
        messages.error(request, 'لا يمكنك حذف حسابك الشخصي')
        return redirect('authentication:users_list')
    
    # Prevent deleting other superusers unless you're a superuser
    if user_to_delete.is_superuser and not request.user.is_superuser:
        messages.error(request, 'لا يمكنك حذف مدير النظام')
        return redirect('authentication:users_list')
    
    if request.method == 'POST':
        try:
            # Soft delete by deactivating
            user_to_delete.is_active = False
            user_to_delete.save()
            
            messages.success(request, f'تم إلغاء تفعيل المستخدم "{user_to_delete.username}" بنجاح')
            return redirect('authentication:users_list')
            
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف المستخدم: {str(e)}')
    
    context = {
        'user_to_delete': user_to_delete,
    }
    
    return render(request, 'authentication/users/delete.html', context)


@login_required
def user_detail_view(request, user_id):
    """
    View user details
    """
    # Check if user has permission to view user details
    if not (request.user.is_superuser or request.user.is_staff or request.user.id == user_id):
        messages.error(request, 'ليس لديك صلاحية لعرض تفاصيل هذا المستخدم')
        return redirect('authentication:dashboard')
    
    user_detail = get_object_or_404(User, id=user_id)
    
    # Show warning if viewing superuser account
    if user_detail.is_superuser:
        messages.info(request, 'هذا حساب مدير عام. لا يمكن تعديله إلا من خلال لوحة الإدارة أو الطرفية')
    
    # Get user statistics
    from core.models import Agent
    try:
        # Check if user is an agent
        agent = Agent.objects.filter(agentUserID=user_detail, isDeleted=False).first()
        
        # Get created records count
        created_items = Item.objects.filter(createdBy=user_detail, isDeleted=False).count()
        created_invoices = InvoiceMaster.objects.filter(createdBy=user_detail, isDeleted=False).count()
        created_customers = CustomerVendor.objects.filter(createdBy=user_detail, isDeleted=False).count()
        
    except Exception as e:
        agent = None
        created_items = created_invoices = created_customers = 0
    
    context = {
        'user_detail': user_detail,
        'agent': agent,
        'created_items': created_items,
        'created_invoices': created_invoices,
        'created_customers': created_customers,
    }
    
    return render(request, 'authentication/users/detail.html', context)


# Agent Management Views

@login_required
def agents_manage_view(request):
    """
    Display list of all agents with search and pagination
    Only accessible by staff users
    """
    # Check if user has permission to manage agents
    if not request.user.is_staff:
        messages.error(request, 'ليس لديك صلاحية لإدارة المناديب')
        return redirect('authentication:dashboard')
    
    from core.models import Agent
    
    # Get search and filter parameters
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()
    
    # Start with all agents
    agents_queryset = Agent.objects.filter(isDeleted=False)
    
    # Apply search filter
    if search_query:
        agents_queryset = agents_queryset.filter(
            Q(agentName__icontains=search_query) |
            Q(agentUsername__icontains=search_query) |
            Q(agentPhone__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter == 'active':
        agents_queryset = agents_queryset.filter(isActive=True)
    elif status_filter == 'inactive':
        agents_queryset = agents_queryset.filter(isActive=False)
    
    # Apply ordering
    agents_queryset = agents_queryset.order_by('-createdAt')
    
    # Apply pagination
    paginator = Paginator(agents_queryset, 20)  # Show 20 agents per page
    page_number = request.GET.get('page')
    agents = paginator.get_page(page_number)
    
    context = {
        'agents': agents,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_agents': Agent.objects.filter(isDeleted=False).count(),
    }
    
    return render(request, 'authentication/agents_manage.html', context)


@login_required
def agent_create_view(request):
    """
    Create a new agent
    Only accessible by staff users with add permission
    """
    # Check permissions
    if not request.user.is_staff:
        messages.error(request, 'ليس لديك صلاحية لإنشاء مناديب جدد')
        return redirect('authentication:agents_manage')
    
    from core.models import Agent, Store
    from django.contrib.auth.hashers import make_password
    
    if request.method == 'POST':
        try:
            # Get form data
            agent_name = request.POST.get('agentName', '').strip()
            agent_username = request.POST.get('agentUsername', '').strip()
            agent_phone = request.POST.get('agentPhone', '').strip()
            agent_password = request.POST.get('agentPassword', '').strip()
            confirm_password = request.POST.get('confirmPassword', '').strip()
            is_active = request.POST.get('isActive') == 'on'
            
            # Validation
            if not agent_name:
                messages.error(request, 'اسم المندوب مطلوب')
                return render(request, 'authentication/agent_create.html')
            
            if not agent_username:
                messages.error(request, 'اسم المستخدم مطلوب')
                return render(request, 'authentication/agent_create.html')
            
            if not agent_password:
                messages.error(request, 'كلمة المرور مطلوبة')
                return render(request, 'authentication/agent_create.html')
            
            if agent_password != confirm_password:
                messages.error(request, 'كلمات المرور غير متطابقة')
                return render(request, 'authentication/agent_create.html')
            
            # Check username uniqueness
            if Agent.objects.filter(agentUsername=agent_username, isDeleted=False).exists():
                messages.error(request, 'اسم المستخدم موجود بالفعل')
                return render(request, 'authentication/agent_create.html')
            
            # Get store_id from form (fix for missing variable)
            store_id = request.POST.get('storeID')
            
            # Create agent
            agent = Agent.objects.create(
                agentName=agent_name,
                agentUsername=agent_username,
                agentPhone=agent_phone if agent_phone else None,
                storeID_id=store_id if store_id else None,
                agentPassword=make_password(agent_password),
                isActive=is_active,
                createdBy=request.user,
                updatedBy=request.user
            )
            
            messages.success(request, f'تم إنشاء المندوب "{agent.agentName}" بنجاح')
            return redirect('authentication:agents_manage')
            
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء إنشاء المندوب: {str(e)}')
    
    # Get all stores for the dropdown
    stores = Store.objects.filter(isDeleted=False).order_by('storeName')
    
    return render(request, 'authentication/agent_create.html', {
        'stores': stores
    })


@login_required
def agent_detail_view(request, agent_id):
    """
    View agent details and their voucher transactions
    Only accessible by staff users
    """
    # Check permissions
    if not request.user.is_staff:
        messages.error(request, 'ليس لديك صلاحية لعرض تفاصيل المناديب')
        return redirect('authentication:dashboard')
    
    from core.models import Agent, Transaction, InvoiceMaster
    from datetime import datetime, timedelta
    from django.db.models import Q
    
    agent = get_object_or_404(Agent, id=agent_id, isDeleted=False)
    
    # Get filter parameters
    transaction_type_filter = request.GET.get('transaction_type', '').strip()
    transaction_id_filter = request.GET.get('transaction_id', '').strip()
    customer_vendor_filter = request.GET.get('customer_vendor', '').strip()
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Build query for actual vouchers only (cash/bank transactions)
    # Type 1: Receipt vouchers (customer payments for sales)
    # Type 2: Payment vouchers (agent payments for returns) - only cash/bank accounts
    # Exclude customer account entries which are just accounting records
    from core.models import Account
    cash_bank_accounts = Account.objects.filter(
        accountName__in=['Store Cash', 'Main Bank', 'Cash', 'Bank']
    ).values_list('id', flat=True)
    
    query = Q(agentID=agent) & Q(isDeleted=False) & Q(accountID__in=cash_bank_accounts)
    
    # Apply transaction type filter
    if transaction_type_filter:
        if transaction_type_filter == 'receipt':
            query &= Q(type=1)
        elif transaction_type_filter == 'payment':
            query &= Q(type=2)
    
    # Apply date filters
    if date_from:
        try:
            date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d').date()
            query &= Q(createdAt__date__gte=date_from_parsed)
        except ValueError:
            messages.warning(request, 'تاريخ البداية غير صحيح')
    
    if date_to:
        try:
            date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d').date()
            query &= Q(createdAt__date__lte=date_to_parsed)
        except ValueError:
            messages.warning(request, 'تاريخ النهاية غير صحيح')
    
    # Apply transaction/invoice ID filter
    if transaction_id_filter:
        query &= Q(Q(id__icontains=transaction_id_filter) | Q(invoiceID__id__icontains=transaction_id_filter))
    
    # Apply customer/vendor filter
    if customer_vendor_filter:
        query &= Q(customerVendorID__id=customer_vendor_filter)
    
    # Get transactions directly using agentID field
    transactions_list = Transaction.objects.filter(query).select_related(
        'accountID', 'customerVendorID'
    ).order_by('-createdAt')
    
    # Apply pagination
    paginator = Paginator(transactions_list, 15)
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)
    
    # Calculate statistics
    total_transactions = transactions_list.count()
    receipt_transactions = transactions_list.filter(type=1).count()
    payment_transactions = transactions_list.filter(type=2).count()
    
    # Get invoices created by this agent
    sales_invoices = InvoiceMaster.objects.filter(
        agentID=agent, 
        invoiceType=2,  # Sales
        isDeleted=False
    ).count()
    
    return_sales_invoices = InvoiceMaster.objects.filter(
        agentID=agent, 
        invoiceType=4,  # Return Sales
        isDeleted=False
    ).count()
    
    # Get customers for the filter dropdown (only customers, not vendors)
    from core.models import CustomerVendor, Visit
    customers = CustomerVendor.objects.filter(isDeleted=False, type=1).order_by('customerVendorName')
    
    # Get visits count for this agent
    visits_count = Visit.objects.filter(agentID=agent, isDeleted=False).count()
    
    # Calculate cash balance (money in minus money out)
    from django.db.models import Sum
    # Receipts (type 1) have positive amounts, payments (type 2) have negative amounts
    # So we just sum all amounts - payments are already negative
    cash_balance = transactions_list.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'agent': agent,
        'transactions': transactions,
        'total_transactions': total_transactions,
        'receipt_transactions': receipt_transactions,
        'payment_transactions': payment_transactions,
        'sales_invoices': sales_invoices,
        'return_sales_invoices': return_sales_invoices,
        'visits_count': visits_count,
        'cash_balance': cash_balance,
        'customers': customers,
        'transaction_type_filter': transaction_type_filter,
        'transaction_id_filter': transaction_id_filter,
        'customer_vendor_filter': customer_vendor_filter,
        'date_from': date_from,
        'date_to': date_to,
        'today_date': timezone.localtime(timezone.now()).date().strftime('%Y-%m-%d'),
    }
    
    return render(request, 'authentication/agent_detail.html', context)


@login_required
def agent_edit_view(request, agent_id):
    """
    Edit an existing agent
    Only accessible by staff users with change permission
    """
    # Check permissions
    if not request.user.is_staff:
        messages.error(request, 'ليس لديك صلاحية لتعديل المناديب')
        return redirect('authentication:agents_manage')
    
    from core.models import Agent, Store
    from django.contrib.auth.hashers import make_password
    
    agent = get_object_or_404(Agent, id=agent_id, isDeleted=False)
    
    if request.method == 'POST':
        try:
            # Get form data
            agent_name = request.POST.get('agentName', '').strip()
            agent_username = request.POST.get('agentUsername', '').strip()
            agent_phone = request.POST.get('agentPhone', '').strip()
            agent_password = request.POST.get('agentPassword', '').strip()
            confirm_password = request.POST.get('confirmPassword', '').strip()
            is_active = request.POST.get('isActive') == 'on'
            
            # Validation
            if not agent_name:
                messages.error(request, 'اسم المندوب مطلوب')
                return render(request, 'authentication/agent_edit.html', {'agent': agent})
            
            if not agent_username:
                messages.error(request, 'اسم المستخدم مطلوب')
                return render(request, 'authentication/agent_edit.html', {'agent': agent})
            
            # Check password confirmation if password is provided
            if agent_password:
                if agent_password != confirm_password:
                    messages.error(request, 'كلمات المرور غير متطابقة')
                    return render(request, 'authentication/agent_edit.html', {'agent': agent})
            
            # Check username uniqueness (excluding current agent)
            if Agent.objects.filter(
                agentUsername=agent_username, 
                isDeleted=False
            ).exclude(id=agent.id).exists():
                messages.error(request, 'اسم المستخدم موجود بالفعل')
                return render(request, 'authentication/agent_edit.html', {'agent': agent})
            
            # Get store_id from form
            store_id = request.POST.get('storeID')
            
            # Update agent
            agent.agentName = agent_name
            agent.agentUsername = agent_username
            agent.agentPhone = agent_phone if agent_phone else None
            agent.storeID_id = store_id if store_id else None
            agent.isActive = is_active
            agent.updatedBy = request.user
            
            # Update password if provided
            if agent_password:
                agent.agentPassword = make_password(agent_password)
            
            agent.save()
            
            messages.success(request, f'تم تحديث المندوب "{agent.agentName}" بنجاح')
            return redirect('authentication:agent_detail', agent_id=agent.id)
            
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء تحديث المندوب: {str(e)}')
    
    # Get all stores for the dropdown
    stores = Store.objects.filter(isDeleted=False).order_by('storeName')
    
    return render(request, 'authentication/agent_edit.html', {
        'agent': agent,
        'stores': stores
    })


@login_required
def agent_delete_view(request, agent_id):
    """
    Delete an agent (soft delete)
    Only accessible by staff users with delete permission
    """
    # Check permissions
    if not request.user.is_staff:
        messages.error(request, 'ليس لديك صلاحية لحذف المناديب')
        return redirect('authentication:agents_manage')
    
    from core.models import Agent
    
    agent = get_object_or_404(Agent, id=agent_id, isDeleted=False)
    
    # Note: Currently there's no direct relationship between Agent and Transaction models
    # Transaction count would need to be implemented if this relationship is added in the future
    transaction_count = 0
    
    if request.method == 'POST':
        try:
            # Soft delete the agent
            agent.isDeleted = True
            agent.deletedBy = request.user
            agent.deletedAt = timezone.now()
            agent.save()
            
            messages.success(request, f'تم حذف المندوب "{agent.agentName}" بنجاح')
            return redirect('authentication:agents_manage')
            
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف المندوب: {str(e)}')
    
    context = {
        'agent': agent,
        'transaction_count': transaction_count,
    }
    
    return render(request, 'authentication/agent_delete.html', context)


# API Endpoints
@csrf_exempt
@api_view(['POST'])
@extend_schema(
    summary="Agent Login",
    description="Login endpoint for agents using username and password"
)
def agent_login_api(request):
    """
    API endpoint for agent authentication
    """
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Only POST method allowed'
        }, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({
                'success': False,
                'message': 'Username and password are required'
            }, status=400)
        
        # Import Agent model
        from core.models import Agent
        
        # Find agent by username
        try:
            agent = Agent.objects.get(agentUsername=username, isDeleted=False)
        except Agent.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Invalid credentials'
            }, status=400)
        
        # Check password
        if check_password(password, agent.agentPassword):
            # Generate simple token (agent ID as token for simplicity)
            token = str(agent.id)
            
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'id': agent.id,
                'name': agent.agentName,
                'token': token,
                'storeID': agent.storeID.id if agent.storeID else None
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid credentials'
            }, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON format'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Server error: {str(e)}'
        }, status=500)


@csrf_exempt
@api_view(['GET'])
@extend_schema(
    summary="Get Agent Sales Invoices",
    description="Get all sales invoices for a specific agent"
)
def agent_invoices_api(request, agent_id):
    """
    API endpoint to get sales invoices for a specific agent
    """
    if request.method != 'GET':
        return JsonResponse({
            'success': False,
            'message': 'Only GET method allowed'
        }, status=405)
    
    try:
        # Import required models
        from core.models import Agent, InvoiceMaster
        
        # Verify agent exists and is not deleted
        try:
            agent = Agent.objects.get(id=agent_id, isDeleted=False)
        except Agent.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Agent not found'
            }, status=404)
        
        # Get sales invoices for this agent (invoiceType = 2 for Sales)
        invoices = InvoiceMaster.objects.filter(
            agentID=agent,
            invoiceType=2,  # Sales invoices only
            isDeleted=False
        ).select_related('customerOrVendorID', 'storeID').order_by('-createdAt')
        
        # Serialize invoice data
        invoices_data = []
        for invoice in invoices:
            invoice_data = {
                'id': invoice.id,
                'customer_name': invoice.customerOrVendorID.name if invoice.customerOrVendorID else None,
                'store_name': invoice.storeID.storeName if invoice.storeID else None,
                'invoice_type': invoice.get_invoiceType_display(),
                'notes': invoice.notes,
                'discount_amount': float(invoice.discountAmount) if invoice.discountAmount else 0,
                'discount_percentage': float(invoice.discountPercentage) if invoice.discountPercentage else 0,
                'tax_amount': float(invoice.taxAmount) if invoice.taxAmount else 0,
                'tax_percentage': float(invoice.taxPercentage) if invoice.taxPercentage else 0,
                'net_total': float(invoice.netTotal) if invoice.netTotal else 0,
                'payment_type': invoice.get_paymentType_display(),
                'status': invoice.get_status_display(),
                'total_paid': float(invoice.totalPaid) if invoice.totalPaid else 0,
                'return_status': invoice.get_returnStatus_display(),
                'created_at': invoice.createdAt.isoformat() if invoice.createdAt else None,
                'updated_at': invoice.updatedAt.isoformat() if invoice.updatedAt else None,
            }
            invoices_data.append(invoice_data)
        
        return JsonResponse({
            'success': True,
            'agent_id': agent.id,
            'agent_name': agent.agentName,
            'invoices_count': len(invoices_data),
            'invoices': invoices_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Server error: {str(e)}'
        }, status=500)


@api_view(['GET'])
def agent_invoices_filtered_api(request):
    """
    API endpoint to get agent invoices filtered by type and date range
    """
    try:
        agent_id = request.GET.get('agent_id')
        invoice_type = request.GET.get('invoice_type')
        transaction_id = request.GET.get('transaction_id')
        customer_vendor = request.GET.get('customer_vendor')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        if not agent_id:
            return JsonResponse({
                'success': False,
                'message': 'Agent ID is required'
            }, status=400)
        
        from core.models import Agent, InvoiceMaster
        from datetime import datetime
        
        # Get agent
        try:
            agent = Agent.objects.get(id=agent_id, isDeleted=False)
        except Agent.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Agent not found'
            }, status=404)
        
        # Build query
        query = Q(agentID=agent, isDeleted=False)
        
        # Filter by invoice type
        if invoice_type:
            query &= Q(invoiceType=int(invoice_type))
        
        # Filter by date range
        if date_from:
            try:
                date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d').date()
                query &= Q(createdAt__date__gte=date_from_parsed)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d').date()
                query &= Q(createdAt__date__lte=date_to_parsed)
            except ValueError:
                pass
        
        # Filter by transaction/invoice ID
        if transaction_id:
            query &= Q(id__icontains=transaction_id)
        
        # Filter by customer/vendor
        if customer_vendor:
            try:
                query &= Q(customerOrVendorID__id=int(customer_vendor))
            except ValueError:
                pass
        
        # Get invoices
        invoices = InvoiceMaster.objects.filter(query).select_related(
            'customerOrVendorID', 'storeID', 'originalInvoiceID'
        ).order_by('-createdAt')[:50]  # Limit to 50 results
        
        invoices_data = []
        for invoice in invoices:
            # Get invoice details for this invoice
            from core.models import InvoiceDetail
            invoice_details = InvoiceDetail.objects.filter(
                invoiceMasterID=invoice,
                isDeleted=False
            ).select_related('item')
            
            # Build invoice details array
            details_data = []
            for detail in invoice_details:
                details_data.append({
                    'itemID': detail.item.id,
                    'itemName': detail.item.itemName,
                    'itemQuantity': float(detail.quantity) if detail.quantity else 0.0
                })
            
            invoice_data = {
                'id': invoice.id,
                'invoiceNumber': f'INV-{invoice.id:06d}',  # Generate invoice number from ID
                'invoiceType': invoice.invoiceType,
                'customerName': invoice.customerOrVendorID.customerVendorName if invoice.customerOrVendorID else None,
                'storeName': invoice.storeID.storeName if invoice.storeID else None,
                'discountAmount': float(invoice.discountAmount) if invoice.discountAmount else 0.0,
                'taxAmount': float(invoice.taxAmount) if invoice.taxAmount else 0.0,
                'netTotal': float(invoice.netTotal) if invoice.netTotal else 0.0,
                'totalPaid': float(invoice.totalPaid) if invoice.totalPaid else 0.0,
                'paymentType': invoice.paymentType,
                'status': invoice.status,  # Use actual status field: 0=paid, 1=unpaid, 2=partially paid
                'originalInvoiceNumber': f'INV-{invoice.originalInvoiceID.id:06d}' if invoice.originalInvoiceID else None,
                'createdAt': invoice.createdAt.isoformat() if invoice.createdAt else None,
                'notes': invoice.notes,
                'invoiceDetails': details_data
            }
            invoices_data.append(invoice_data)
        
        return JsonResponse({
            'success': True,
            'agent_id': agent.id,
            'agent_name': agent.agentName,
            'invoice_type': invoice_type,
            'invoices_count': len(invoices_data),
            'invoices': invoices_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Server error: {str(e)}'
        }, status=500)


@api_view(['GET'])
def agent_transactions_filtered_api(request):
    """
    API endpoint to get agent transactions (vouchers) filtered by type and date range
    """
    try:
        agent_id = request.GET.get('agent_id')
        transaction_type = request.GET.get('transaction_type')
        transaction_id = request.GET.get('transaction_id')
        customer_vendor = request.GET.get('customer_vendor')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        if not agent_id:
            return JsonResponse({
                'success': False,
                'message': 'Agent ID is required'
            }, status=400)
        
        from core.models import Agent, Transaction
        from datetime import datetime
        
        # Get agent
        try:
            agent = Agent.objects.get(id=agent_id, isDeleted=False)
        except Agent.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Agent not found'
            }, status=404)
        
        # Build query for actual vouchers only (cash/bank transactions)
        # Type 1: Receipt vouchers (customer payments for sales)
        # Type 2: Payment vouchers (agent payments for returns) - only cash/bank accounts
        # Exclude customer account entries which are just accounting records
        from core.models import Account
        cash_bank_accounts = Account.objects.filter(
            accountName__in=['Store Cash', 'Main Bank', 'Cash', 'Bank']
        ).values_list('id', flat=True)
        
        query = Q(agentID=agent) & Q(isDeleted=False) & Q(accountID__in=cash_bank_accounts)
        
        # Filter by transaction type
        if transaction_type:
            query &= Q(type=int(transaction_type))
        
        # Filter by date range
        if date_from:
            try:
                date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d').date()
                query &= Q(createdAt__date__gte=date_from_parsed)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d').date()
                query &= Q(createdAt__date__lte=date_to_parsed)
            except ValueError:
                pass
        
        # Filter by transaction/invoice ID
        if transaction_id:
            query &= Q(Q(id__icontains=transaction_id) | Q(invoiceID__id__icontains=transaction_id))
        
        # Filter by customer/vendor
        if customer_vendor:
            try:
                query &= Q(customerVendorID__id=int(customer_vendor))
            except ValueError:
                pass
        
        # Get transactions created by this agent
        all_transactions = Transaction.objects.filter(query).select_related(
            'accountID', 'customerVendorID', 'invoiceID'
        ).order_by('-createdAt')
        
        # Filter for cash/payment transactions only (receipts and payments)
        payment_transactions = []
        for transaction in all_transactions:
            # Include cash account transactions (Account ID 35 = Cash, 10 = Bank/Visa)
            if transaction.accountID and transaction.accountID.id in [35, 10]:
                # For receipt vouchers (type 1): positive amounts in cash accounts
                # For payment vouchers (type 2): negative amounts in cash accounts
                if ((transaction_type == '1' and transaction.amount > 0) or 
                    (transaction_type == '2' and transaction.amount < 0) or
                    (not transaction_type)):  # Include all if no type filter
                    payment_transactions.append(transaction)
        
        # Limit results and sort by creation date
        transactions_list = payment_transactions[:50]
        
        transactions_data = []
        for transaction in transactions_list:
            # Determine transaction type display
            transaction_type_display = 1 if transaction.amount > 0 else 2  # 1=Receipt, 2=Payment
            
            transaction_data = {
                'id': transaction.id,
                'voucherNumber': f"INV-{transaction.invoiceID.id}" if transaction.invoiceID else f"TXN-{transaction.id}",
                'type': transaction_type_display,
                'amount': float(abs(transaction.amount)) if transaction.amount else 0.0,  # Use absolute value for display
                'customerName': transaction.customerVendorID.customerVendorName if transaction.customerVendorID else None,
                'notes': transaction.notes or (f"Invoice #{transaction.invoiceID.id}" if transaction.invoiceID else "Manual Transaction"),
                'createdAt': transaction.createdAt.isoformat() if transaction.createdAt else None,
                'invoiceId': transaction.invoiceID.id if transaction.invoiceID else None
            }
            transactions_data.append(transaction_data)
        
        return JsonResponse({
            'success': True,
            'agent_id': agent.id,
            'agent_name': agent.agentName,
            'transaction_type': transaction_type,
            'transactions_count': len(transactions_data),
            'transactions': transactions_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Server error: {str(e)}'
        }, status=500)


def get_agent_basic_auth(request):
    """
    Helper function to handle Basic Auth for Agent model
    Returns tuple (agent, error_response)
    If authentication successful: returns (agent, None)
    If authentication failed: returns (None, JsonResponse)
    """
    import base64
    from django.contrib.auth.hashers import check_password
    from core.models import Agent

    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or not auth_header.startswith('Basic '):
        return None, JsonResponse({
            'success': False,
            'message': 'Authentication credentials were not provided.'
        }, status=401, headers={'WWW-Authenticate': 'Basic realm="Agent API"'})

    try:
        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded_credentials.split(':', 1)
    except Exception:
        return None, JsonResponse({
            'success': False,
            'message': 'Invalid authentication credentials.'
        }, status=401, headers={'WWW-Authenticate': 'Basic realm="Agent API"'})

    try:
        agent = Agent.objects.get(agentUsername=username, isDeleted=False)
    except Agent.DoesNotExist:
        return None, JsonResponse({
            'success': False,
            'message': 'Invalid username or password.'
        }, status=401, headers={'WWW-Authenticate': 'Basic realm="Agent API"'})

    if not agent.isActive:
        return None, JsonResponse({
            'success': False,
            'message': 'Agent account is inactive.'
        }, status=403)

    if not check_password(password, agent.agentPassword):
        return None, JsonResponse({
            'success': False,
            'message': 'Invalid username or password.'
        }, status=401, headers={'WWW-Authenticate': 'Basic realm="Agent API"'})

    return agent, None


@csrf_exempt
@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def customer_transactions_api(request):
    """
    API endpoint to get transactions for customers assigned to the authenticated agent
    """
    # 1. Authenticate Agent
    agent, error_response = get_agent_basic_auth(request)
    if error_response:
        return error_response

    try:
        from core.models import VisitPlan, Transaction
        
        # 2. Get active VisitPlan for the agent
        visit_plan = VisitPlan.objects.filter(
            agentID=agent,
            isActive=True,
            isDeleted=False
        ).first()

        if not visit_plan:
            return JsonResponse({
                'success': True,
                'message': 'No active visit plan found.',
                'transactions': []
            })

        # 3. Extract customer IDs
        customer_ids = visit_plan.customers
        if not customer_ids or not isinstance(customer_ids, list):
             return JsonResponse({
                'success': True,
                'message': 'No customers assigned in the visit plan.',
                'transactions': []
            })

        # 4. Query Transactions - Get all relevant transactions (Invoices and Payments)
        transactions = Transaction.objects.filter(
            customerVendorID__id__in=customer_ids,
            isDeleted=False,
            # type__in=[1, 2]  # 1=Purchase/Receipt, 2=Sales/Payment
        ).select_related('customerVendorID', 'invoiceID').order_by('customerVendorID__id', '-createdAt')

        # 5. Format Response - Group by customer
        from collections import defaultdict
        grouped_transactions = defaultdict(list)
        
        for trans in transactions:
            customer_id = trans.customerVendorID.id if trans.customerVendorID else None
            customer_name = trans.customerVendorID.customerVendorName if trans.customerVendorID else 'Unknown'
            
            trans_data = {
                'created_at': trans.createdAt.isoformat() if trans.createdAt else None,
                'amount': float(trans.amount) if trans.amount else 0.0,
                'notes': trans.notes,
                'type': trans.type,
                'invoiceID': trans.invoiceID.id if trans.invoiceID else None,
                'accountID': trans.accountID_id
            }
            
            if customer_id:
                grouped_transactions[customer_id].append({
                    'customer_id': customer_id,
                    'customer_name': customer_name,
                    'transaction': trans_data
                })

        # Convert to list format
        result_data = []
        for customer_id, trans_list in grouped_transactions.items():
            if trans_list:
                customer_name = trans_list[0]['customer_name']
                result_data.append({
                    'customer_id': customer_id,
                    'customer_name': customer_name,
                    'transactions': [item['transaction'] for item in trans_list]
                })

        return JsonResponse({
            'success': True,
            'count': len(transactions),
            'customers_count': len(result_data),
            'data': result_data
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Server error: {str(e)}'
        }, status=500)

