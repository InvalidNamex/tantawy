from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='reports_index'),
    path('customer-purchase-history/', views.customer_purchase_history, name='customer_purchase_history'),
    path('top-customers/', views.top_customers, name='top_customers'),
    path('customer-balance/', views.customer_balance, name='customer_balance'),
    path('product-sales-by-customer/', views.product_sales_by_customer, name='product_sales_by_customer'),
    path('invoice-transaction-summary/', views.invoice_transaction_summary, name='invoice_transaction_summary'),
]
