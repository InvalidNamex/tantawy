# Views for customer-focused reports

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from core.models import CustomerVendor, InvoiceDetail, InvoiceMaster

@login_required
def index(request):
    """Main reports landing page."""
    return render(request, 'reports/index.html')


@login_required
def customer_purchase_history(request):
    customers = CustomerVendor.objects.filter(type__in=[1,3], isDeleted=False)
    selected_customer = request.GET.get('customer')
    purchases = []
    net_total = 0
    grouped_invoices = []
    if selected_customer:
        purchases = InvoiceDetail.objects.filter(
            invoiceMasterID__customerOrVendorID_id=selected_customer,
            invoiceMasterID__invoiceType__in=[2, 4],  # Sales and Return Sales
            isDeleted=False,
            invoiceMasterID__isDeleted=False
        ).select_related('item', 'invoiceMasterID')
        # Group items by invoice
        invoice_map = {}
        for p in purchases:
            invoice_id = p.invoiceMasterID.id
            if invoice_id not in invoice_map:
                invoice_map[invoice_id] = {
                    'invoice': p.invoiceMasterID,
                    'items': [],
                    'total': 0,
                }
            total = (p.quantity or 0) * (p.price or 0)
            invoice_map[invoice_id]['items'].append({
                'item': p.item,
                'quantity': p.quantity,
                'price': p.price,
                'total': total,
            })
            invoice_map[invoice_id]['total'] += total
            if p.invoiceMasterID.invoiceType == 2:
                net_total += total
            elif p.invoiceMasterID.invoiceType == 4:
                net_total -= total
        grouped_invoices = list(invoice_map.values())
    
    return render(request, 'reports/customer_purchase_history.html', {
        'customers': customers,
        'selected_customer': int(selected_customer) if selected_customer else None,
        'grouped_invoices': grouped_invoices,
        'net_total': net_total,
    })


@login_required
def top_customers(request):
    """Top customers ranked by net sales."""
    limit = request.GET.get('limit', '20')
    
    # Get all customers
    customers = CustomerVendor.objects.filter(type__in=[1, 3], isDeleted=False)
    
    customer_stats = []
    total_revenue = 0
    
    for customer in customers:
        # Get all invoice details for this customer
        purchases = InvoiceDetail.objects.filter(
            invoiceMasterID__customerOrVendorID_id=customer.id,
            invoiceMasterID__invoiceType__in=[2, 4],  # Sales and Return Sales
            isDeleted=False,
            invoiceMasterID__isDeleted=False
        ).select_related('invoiceMasterID')
        
        sales_total = 0
        returns_total = 0
        invoice_count = set()
        item_count = 0
        
        for p in purchases:
            total = (p.quantity or 0) * (p.price or 0)
            invoice_count.add(p.invoiceMasterID.id)
            item_count += 1
            
            if p.invoiceMasterID.invoiceType == 2:  # Sales
                sales_total += total
            elif p.invoiceMasterID.invoiceType == 4:  # Return Sales
                returns_total += total
        
        net_sales = sales_total - returns_total
        
        if net_sales > 0 or sales_total > 0 or returns_total > 0:  # Only include customers with transactions
            customer_stats.append({
                'customer': customer,
                'sales_total': sales_total,
                'returns_total': returns_total,
                'net_sales': net_sales,
                'invoice_count': len(invoice_count),
                'item_count': item_count,
            })
            total_revenue += net_sales
    
    # Sort by net sales descending
    customer_stats.sort(key=lambda x: x['net_sales'], reverse=True)
    
    # Apply limit
    if limit != 'all':
        try:
            limit_int = int(limit)
            customer_stats = customer_stats[:limit_int]
        except ValueError:
            customer_stats = customer_stats[:20]
    
    # Calculate max for progress bars
    max_sales = customer_stats[0]['net_sales'] if customer_stats else 0
    
    # Add rank and percentage for each customer
    for idx, stat in enumerate(customer_stats, 1):
        stat['rank'] = idx
        stat['percentage'] = (stat['net_sales'] / max_sales * 100) if max_sales > 0 else 0
    
    return render(request, 'reports/top_customers.html', {
        'customer_stats': customer_stats,
        'total_customers': len(customer_stats),
        'total_revenue': total_revenue,
        'average_revenue': total_revenue / len(customer_stats) if customer_stats else 0,
        'selected_limit': limit,
        'max_sales': max_sales,
    })


@login_required
def customer_balance(request):
    """Customer balance and outstanding payments report."""
    from core.models import Transaction, Agent, VisitPlan
    from django.db import connection
    
    status_filter = request.GET.get('status', 'all')
    sort_by = request.GET.get('sort', 'balance')
    sort_direction = request.GET.get('direction', 'asc')
    search_query = request.GET.get('search', '').strip()
    agent_filter = request.GET.get('agent', '')
    
    # Get all agents for the dropdown
    agents = Agent.objects.filter(isDeleted=False, isActive=True).order_by('agentName')
    
    # Get all customers
    customers = CustomerVendor.objects.filter(type__in=[1, 3], isDeleted=False)
    
    # Apply agent filter - get customers from agent's active visit plan
    if agent_filter:
        try:
            agent_id = int(agent_filter)
            active_plan = VisitPlan.objects.filter(
                agentID_id=agent_id,
                isActive=True,
                isDeleted=False
            ).first()
            
            if active_plan and active_plan.customers:
                # Filter customers to only those in the active visit plan
                customer_ids = active_plan.customers  # This is a JSON array of customer IDs
                customers = customers.filter(id__in=customer_ids)
            else:
                # Agent has no active plan, show no customers
                customers = customers.none()
        except (ValueError, TypeError):
            pass
    
    # Apply search filter
    if search_query:
        customers = customers.filter(customerVendorName__icontains=search_query)
    
    customer_balances = []
    total_outstanding = 0
    total_credit_balance = 0
    outstanding_count = 0
    credit_count = 0
    paid_count = 0
    
    # Use raw SQL to calculate balances from all customer transactions
    with connection.cursor() as cursor:
        for customer in customers:
            # Query all transactions for this customer
            # Positive amount = debit (payment received from customer)
            # Negative amount = credit (sale/amount owed by customer)
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END), 0) as total_debit,
                    COALESCE(SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END), 0) as total_credit,
                    COUNT(*) as transaction_count,
                    MAX("createdAt") as last_transaction
                FROM transactions
                WHERE "customerVendorID_id" = %s 
                  AND "isDeleted" = FALSE
            """, [customer.id])
            
            row = cursor.fetchone()
            total_debit = float(row[0]) if row[0] else 0
            total_credit = float(row[1]) if row[1] else 0
            transaction_count = row[2] if row[2] else 0
            last_transaction = row[3]
            
            # Calculate balance
            # Balance = total_debit - total_credit
            # Negative balance means customer owes us money (outstanding)
            # Positive balance means we owe customer money (credit balance)
            balance = total_debit - total_credit
            
            # Determine status
            if balance < -0.01:  # Customer owes us (outstanding)
                status = 'outstanding'
                outstanding_count += 1
                total_outstanding += abs(balance)
            elif balance > 0.01:  # We owe customer (credit)
                status = 'credit'
                credit_count += 1
                total_credit_balance += balance
            else:  # Fully paid
                status = 'paid'
                paid_count += 1
            
            customer_balances.append({
                'customer': customer,
                'total_debit': total_debit,
                'total_credit': total_credit,
                'balance': balance,
                'transaction_count': transaction_count,
                'last_transaction': last_transaction,
                'status': status,
            })
    
    # Calculate total customers before applying filter
    total_customers = len(customer_balances)
    
    # Apply status filter
    if status_filter != 'all':
        customer_balances = [cb for cb in customer_balances if cb['status'] == status_filter]
    
    # Apply sorting
    reverse = (sort_direction == 'desc')
    if sort_by == 'balance':
        customer_balances.sort(key=lambda x: x['balance'], reverse=reverse)
    elif sort_by == 'name':
        customer_balances.sort(key=lambda x: x['customer'].customerVendorName, reverse=reverse)
    elif sort_by == 'last_transaction':
        customer_balances.sort(key=lambda x: x['last_transaction'] or '', reverse=reverse)
    
    return render(request, 'reports/customer_balance.html', {
        'customer_balances': customer_balances,
        'total_customers': total_customers,
        'outstanding_count': outstanding_count,
        'total_outstanding': total_outstanding,
        'credit_count': credit_count,
        'total_credit': total_credit_balance,
        'paid_count': paid_count,
        'selected_status': status_filter,
        'selected_sort': sort_by,
        'selected_direction': sort_direction,
        'search_query': search_query,
        'agents': agents,
        'selected_agent': agent_filter,
    })


@login_required
def product_sales_by_customer(request):
    """Product sales breakdown by customer."""
    customers = CustomerVendor.objects.filter(type__in=[1, 3], isDeleted=False)
    selected_customer = request.GET.get('customer')
    sort_by = request.GET.get('sort', 'quantity')
    
    product_sales = []
    total_products = 0
    total_sales = 0
    top_product = None
    
    if selected_customer:
        # Get all invoice details for this customer (sales only, not returns)
        purchases = InvoiceDetail.objects.filter(
            invoiceMasterID__customerOrVendorID_id=selected_customer,
            invoiceMasterID__invoiceType=2,  # Sales only
            isDeleted=False,
            invoiceMasterID__isDeleted=False
        ).select_related('item', 'invoiceMasterID')
        
        # Group by product
        product_map = {}
        for p in purchases:
            if not p.item:
                continue
                
            item_id = p.item.id
            if item_id not in product_map:
                product_map[item_id] = {
                    'product': p.item,
                    'quantity': 0,
                    'total_amount': 0,
                    'invoice_count': set(),
                }
            
            quantity = p.quantity or 0
            price = p.price or 0
            amount = quantity * price
            
            product_map[item_id]['quantity'] += quantity
            product_map[item_id]['total_amount'] += amount
            product_map[item_id]['invoice_count'].add(p.invoiceMasterID.id)
        
        # Convert to list and calculate totals
        for item_id, data in product_map.items():
            total_sales += data['total_amount']
            product_sales.append({
                'product': data['product'],
                'quantity': data['quantity'],
                'total_amount': data['total_amount'],
                'invoice_count': len(data['invoice_count']),
                'avg_price': data['total_amount'] / data['quantity'] if data['quantity'] > 0 else 0,
            })
        
        total_products = len(product_sales)
        
        # Sort products
        if sort_by == 'quantity':
            product_sales.sort(key=lambda x: x['quantity'], reverse=True)
        elif sort_by == 'amount':
            product_sales.sort(key=lambda x: x['total_amount'], reverse=True)
        
        # Calculate percentages and add ranks
        for idx, ps in enumerate(product_sales, 1):
            ps['rank'] = idx
            ps['percentage'] = (ps['total_amount'] / total_sales * 100) if total_sales > 0 else 0
        
        # Get top product
        if product_sales:
            top_product = product_sales[0]
    
    return render(request, 'reports/product_sales_by_customer.html', {
        'customers': customers,
        'selected_customer': int(selected_customer) if selected_customer else None,
        'product_sales': product_sales,
        'total_products': total_products,
        'total_sales': total_sales,
        'average_per_product': total_sales / total_products if total_products > 0 else 0,
        'top_product': top_product,
        'selected_sort': sort_by,
    })


@login_required
def invoice_transaction_summary(request):
    """Comprehensive invoice and transaction summary report."""
    from core.models import Transaction
    from django.db import connection
    from datetime import datetime, timedelta
    
    # Get date filters
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Base query for invoices
    invoices = InvoiceMaster.objects.filter(isDeleted=False)
    
    # Apply date filters
    if date_from:
        invoices = invoices.filter(createdAt__gte=date_from)
    if date_to:
        invoices = invoices.filter(createdAt__lte=date_to)
    
    # Invoice statistics by type
    invoice_stats = {
        'sales': {'count': 0, 'total': 0},
        'returns': {'count': 0, 'total': 0},
        'purchases': {'count': 0, 'total': 0},
        'return_purchases': {'count': 0, 'total': 0},
    }
    
    total_invoices = 0
    
    for invoice in invoices:
        # Get invoice details to calculate total
        details = InvoiceDetail.objects.filter(
            invoiceMasterID=invoice,
            isDeleted=False
        )
        
        invoice_total = sum((d.quantity or 0) * (d.price or 0) for d in details)
        total_invoices += 1
        
        if invoice.invoiceType == 1:  # Purchase
            invoice_stats['purchases']['count'] += 1
            invoice_stats['purchases']['total'] += invoice_total
        elif invoice.invoiceType == 2:  # Sales
            invoice_stats['sales']['count'] += 1
            invoice_stats['sales']['total'] += invoice_total
        elif invoice.invoiceType == 3:  # Return Purchase
            invoice_stats['return_purchases']['count'] += 1
            invoice_stats['return_purchases']['total'] += invoice_total
        elif invoice.invoiceType == 4:  # Return Sales
            invoice_stats['returns']['count'] += 1
            invoice_stats['returns']['total'] += invoice_total
    
    # Transaction statistics
    transactions = Transaction.objects.filter(isDeleted=False)
    
    if date_from:
        transactions = transactions.filter(createdAt__gte=date_from)
    if date_to:
        transactions = transactions.filter(createdAt__lte=date_to)
    
    total_transactions = transactions.count()
    
    # Calculate debits and credits using raw SQL
    with connection.cursor() as cursor:
        where_clause = "WHERE \"isDeleted\" = FALSE"
        params = []
        
        if date_from:
            where_clause += " AND \"createdAt\" >= %s"
            params.append(date_from)
        if date_to:
            where_clause += " AND \"createdAt\" <= %s"
            params.append(date_to)
        
        cursor.execute(f"""
            SELECT 
                COALESCE(SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END), 0) as total_debit,
                COALESCE(SUM(CASE WHEN amount < 0 THEN ABS(amount) ELSE 0 END), 0) as total_credit
            FROM transactions
            {where_clause}
        """, params)
        
        row = cursor.fetchone()
        total_debit = float(row[0]) if row[0] else 0
        total_credit = float(row[1]) if row[1] else 0
    
    net_balance = total_debit - total_credit
    
    # Get top invoices by amount
    top_invoices = []
    for invoice in invoices.order_by('-createdAt')[:10]:
        details = InvoiceDetail.objects.filter(
            invoiceMasterID=invoice,
            isDeleted=False
        )
        invoice_total = sum((d.quantity or 0) * (d.price or 0) for d in details)
        
        top_invoices.append({
            'invoice': invoice,
            'total': invoice_total,
        })
    
    # Sort by total descending
    top_invoices.sort(key=lambda x: x['total'], reverse=True)
    top_invoices = top_invoices[:10]
    
    # Get recent transactions
    recent_transactions = transactions.select_related('customerVendorID', 'invoiceID').order_by('-createdAt')[:15]
    
    # Calculate net sales (sales - returns)
    net_sales = invoice_stats['sales']['total'] - invoice_stats['returns']['total']
    
    return render(request, 'reports/invoice_transaction_summary.html', {
        'total_invoices': total_invoices,
        'invoice_stats': invoice_stats,
        'total_transactions': total_transactions,
        'total_debit': total_debit,
        'total_credit': total_credit,
        'net_balance': net_balance,
        'net_sales': net_sales,
        'top_invoices': top_invoices,
        'recent_transactions': recent_transactions,
        'date_from': date_from,
        'date_to': date_to,
    })
