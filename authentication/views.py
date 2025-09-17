from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.db.models import Count
from core.models import ItemsGroup, Item, PriceList, Store, StoreGroup


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
                    messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                    
                    # Redirect to next page if specified, otherwise to dashboard
                    next_page = request.GET.get('next', 'authentication:dashboard')
                    return redirect(next_page)
                else:
                    messages.error(request, 'Your account is disabled. Please contact administrator.')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Please provide both username and password.')
    
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
    messages.success(request, f'Goodbye {username}! You have been logged out successfully.')
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
    except Exception as e:
        # In case of database issues, set counts to 0
        items_groups_count = items_count = price_lists_count = store_groups_count = stores_count = 0
        messages.warning(request, 'Unable to load statistics. Please check database connection.')
    
    context = {
        'items_groups_count': items_groups_count,
        'items_count': items_count,
        'price_lists_count': price_lists_count,
        'store_groups_count': store_groups_count,
        'stores_count': stores_count,
        'user': request.user,
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
