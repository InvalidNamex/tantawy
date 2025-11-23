from django.urls import path
from . import views
from . import invoice_api

# URLConf
app_name = 'core'

urlpatterns = [
    # Frontend Template-based URLs
    
    # Invoice Management URLs (Template-based for frontend)
    path('invoices/', views.invoices_main_view, name='invoices_main'),
    path('invoices/<int:invoice_id>/', views.invoice_detail_view, name='invoice_detail'),
    path('invoices/purchase/', views.invoices_purchase_view, name='invoices_purchase'),
    path('invoices/sales/', views.invoices_sales_view, name='invoices_sales'),
    path('invoices/return-purchase/', views.invoices_return_purchase_view, name='invoices_return_purchase'),
    path('invoices/return-sales/', views.invoices_return_sales_view, name='invoices_return_sales'),
    
    # Items URLs (Template-based for frontend)
    path('items/', views.items_view, name='items'),
    path('items/add/', views.items_add_view, name='items_add'),
    path('items/<int:item_id>/detail/', views.items_detail_view, name='items_detail'),
    path('items/<int:item_id>/update-main-info/', views.items_update_main_info_view, name='items_update_main_info'),
    path('items/<int:item_id>/add-price/', views.items_add_price_view, name='items_add_price'),
    path('items/<int:item_id>/price/<int:price_id>/', views.items_update_price_view, name='items_update_price'),
    path('items/<int:item_id>/price/<int:price_id>/', views.items_delete_price_view, name='items_delete_price'),
    path('items/edit/<int:item_id>/', views.items_edit_view, name='items_edit'),
    path('items/delete/<int:item_id>/', views.items_delete_view, name='items_delete'),
    path('items/upload-image/', views.items_upload_image_view, name='items_upload_image'),
    
    # ItemsGroups URLs (Template-based for frontend)
    path('itemsgroups/', views.itemsgroups_view, name='itemsgroups'),
    path('itemsgroups/add/', views.itemsgroups_add_view, name='itemsgroups_add'),
    path('itemsgroups/edit/<int:group_id>/', views.itemsgroups_edit_view, name='itemsgroups_edit'),
    path('itemsgroups/delete/<int:group_id>/', views.itemsgroups_delete_view, name='itemsgroups_delete'),
    
    # Customers URLs (Template-based for frontend)
    path('customers/', views.customers_view, name='customers'),
    path('customers/add/', views.customers_add_view, name='customers_add'),
    path('customers/edit/<int:customer_id>/', views.customers_edit_view, name='customers_edit'),
    path('customers/delete/<int:customer_id>/', views.customers_delete_view, name='customers_delete'),
    
    # Vendors URLs (Template-based for frontend)
    path('vendors/', views.vendors_view, name='vendors'),
    path('vendors/add/', views.vendors_add_view, name='vendors_add'),
    path('vendors/edit/<int:vendor_id>/', views.vendors_edit_view, name='vendors_edit'),
    path('vendors/delete/<int:vendor_id>/', views.vendors_delete_view, name='vendors_delete'),
    
    # PriceList URLs (Template-based for frontend)
    path('pricelists/', views.pricelists_view, name='pricelists'),
    path('pricelists/add/', views.pricelist_add_view, name='pricelists_add'),
    path('pricelists/edit/<int:id>/', views.pricelist_edit_view, name='pricelists_edit'),
    path('pricelists/delete/<int:id>/', views.pricelist_delete_view, name='pricelists_delete'),
    
    # StoreGroups URLs (Template-based for frontend)
    path('storegroups/', views.storegroups_view, name='storegroups'),
    path('storegroups/add/', views.storegroup_add_view, name='storegroups_add'),
    path('storegroups/edit/<int:id>/', views.storegroup_edit_view, name='storegroups_edit'),
    path('storegroups/delete/<int:id>/', views.storegroup_delete_view, name='storegroups_delete'),
    
    # Stores URLs (Template-based for frontend)
    path('stores/', views.stores_view, name='stores'),
    path('stores/add/', views.stores_add_view, name='stores_add'),
    path('stores/edit/<int:store_id>/', views.stores_edit_view, name='stores_edit'),
    path('stores/delete/<int:store_id>/', views.stores_delete_view, name='stores_delete'),
    
    # Visit Plans URLs (Template-based for frontend)
    path('visitplans/', views.visitplans_manage_view, name='visitplans_manage'),
    path('visitplans/add/', views.visitplan_add_view, name='visitplan_add'),
    path('visitplans/edit/<int:plan_id>/', views.visitplan_edit_view, name='visitplan_edit'),
    path('visitplans/delete/<int:plan_id>/', views.visitplan_delete_view, name='visitplan_delete'),
    
    # Inventory Management URLs (Template-based for StoreAdmins)
    path('inventory/', views.inventory_management_view, name='inventory_management'),
    path('inventory/store/<int:store_id>/', views.inventory_store_detail_view, name='inventory_store_detail'),
    path('inventory/add-quantity/', views.inventory_add_quantity_view, name='inventory_add_quantity'),
    path('inventory/deduct-quantity/', views.inventory_deduct_quantity_view, name='inventory_deduct_quantity'),
    
    # API URLs - All under /api/ prefix
    
    # ItemsGroup URLs (API)
    path('api/items-groups/', views.itemsgroup_list, name='itemsgroup_list'),
    path('api/items-groups/<int:id>/', views.itemsgroup_detail, name='itemsgroup_detail'),
    
    # Item URLs (API)
    path('api/items/', views.item_list, name='item_list'),
    path('api/items/<int:id>/', views.item_detail, name='item_detail'),
    path('api/items/group/<int:group_id>/', views.item_by_group, name='item_by_group'),
    
    # PriceList URLs (API)
    path('api/price-lists/', views.pricelist_list, name='pricelist_list'),
    path('api/price-lists/<int:id>/', views.pricelist_detail, name='pricelist_detail'),
    
    # PriceListDetail URLs (API)
    path('api/price-list-details/', views.pricelistdetail_list, name='pricelistdetail_list'),
    path('api/price-list-details/pricelist/<int:pricelist_id>/', views.pricelistdetail_by_pricelist, name='pricelistdetail_by_pricelist'),
    
    # StoreGroup URLs (API)
    path('api/store-groups/', views.storegroup_list, name='storegroup_list'),
    path('api/store-groups/<int:id>/', views.storegroup_detail, name='storegroup_detail'),
    
    # Store URLs (API)
    path('api/stores/', views.store_list, name='store_list'),
    path('api/stores/<int:id>/', views.store_detail, name='store_detail'),
    
    # CustomerVendor URLs (API)
    path('api/customers-vendors/', views.customervendor_list, name='customervendor_list'),
    path('api/customers-vendors/<int:id>/', views.customervendor_detail, name='customervendor_detail'),
    
    # InvoiceMaster URLs (API)
    path('api/invoices/', views.invoicemaster_list, name='invoicemaster_list'),
    path('api/invoices/<int:id>/', views.invoicemaster_detail, name='invoicemaster_detail'),
    
    # InvoiceDetail URLs (API)
    path('api/invoice-details/', views.invoicedetail_list, name='invoicedetail_list'),
    path('api/invoice-details/<int:id>/', views.invoicedetail_detail, name='invoicedetail_detail'),
    
    # Stock URLs (API)
    path('api/stock/', views.item_stock, name='item_stock'),
    
    # Account URLs (API)
    path('api/accounts/', views.account_list, name='account_list'),
    path('api/accounts/<int:id>/', views.account_detail, name='account_detail'),
    path('api/accounts/create/', views.account_create, name='account_create'),
    
    # Transaction URLs (API)
    path('api/transactions/', views.transaction_list, name='transaction_list'),
    path('api/transactions/<int:id>/', views.transaction_detail, name='transaction_detail'),
    path('api/transactions/create/', views.transaction_create, name='transaction_create'),
    
    # Agent URLs (API)
    path('api/agents/', views.agent_list, name='agent_list'),
    path('api/agents/<int:id>/', views.agent_detail, name='agent_detail'),
    path('api/agents/create/', views.agent_create, name='agent_create'),
    path('api/agents/<int:id>/update/', views.agent_update, name='agent_update'),
    path('api/agents/<int:id>/delete/', views.agent_delete, name='agent_delete'),
    
    # Agent Transactions URL (API for mobile app to get vouchers)
    path('api/agents/transactions/', views.agent_transactions_api, name='agent_transactions_api'),
    
    # Agent Authentication URLs (API for mobile app)
    path('api/agents/login/', views.agent_login, name='agent_login'),
    path('api/agents/logout/', views.agent_logout, name='agent_logout'),
    path('api/agents/verify-token/', views.agent_verify_token, name='agent_verify_token'),
    
    # Store Authentication URLs (API)
    path('api/stores/login/', views.store_login, name='store_login'),
    path('api/stores/agents/', views.store_agents, name='store_agents'),
    path('api/stores/stock/', views.store_stock, name='store_stock'),
    path('api/stores/update-stock/', views.store_update_stock, name='store_update_stock'),
    
    # Voucher URLs (API for agents)
    path('api/vouchers/', views.create_voucher, name='create_voucher'),
    path('api/vouchers/batch-create/', views.batch_create_vouchers, name='batch_create_vouchers'),
    path('api/vouchers/list/', views.get_vouchers, name='get_vouchers'),
    
    # Invoice API URLs
    path('api/invoices/create/', invoice_api.create_invoice_api, name='create_invoice_api'),
    path('api/invoices/batch-create/', invoice_api.batch_create_invoices_api, name='batch_create_invoices_api'),
    path('api/invoices/<int:invoice_id>/available-returns/', invoice_api.get_available_returns_api, name='get_available_returns_api'),
    path('api/invoices/type/<int:invoice_type>/', invoice_api.get_invoices_by_type_api, name='get_invoices_by_type_api'),
    path('api/invoices/<int:invoice_id>/detail/', invoice_api.get_invoice_detail_api, name='get_invoice_detail_api'),
    
    # Visits API URLs (Agent Authentication Required)
    path('api/visits/create/', views.create_visit, name='create_visit'),
    path('api/visits/batch-create/', views.batch_create_visits, name='batch_create_visits'),
    path('api/visits/list/', views.agent_visits_list, name='agent_visits_list'),
    path('api/visits/agent/<int:agent_id>/', views.agent_visits_list, name='agent_visits_by_id'),
    path('api/visits/negative/', views.get_negative_visits, name='get_negative_visits'),
    
    # VisitPlan API URLs
    path('api/visit-plans/', views.visitplan_list, name='visitplan_list'),
    path('api/visit-plans/<int:id>/', views.visitplan_detail, name='visitplan_detail'),
    path('api/visit-plans/create/', views.visitplan_create, name='visitplan_create'),
    path('api/visit-plans/<int:id>/update/', views.visitplan_update, name='visitplan_update'),
    path('api/visit-plans/<int:id>/delete/', views.visitplan_delete, name='visitplan_delete'),
    
    # Agent VisitPlan URLs (Agent Authentication Required)
    path('api/agents/visit-plans/current/', views.agent_current_visitplan, name='agent_current_visitplan'),
    path('api/agents/visit-plans/list/', views.agent_visitplans_list, name='agent_visitplans_list'),
    path('api/agents/visit-plans/active-with-customers/', views.agent_active_plan_with_customers, name='agent_active_plan_with_customers'),
    
    # Agent Stock URL (API for mobile app)
    path('api/agents/stock/', views.agent_stock, name='agent_stock'),
    
    # Agent Cash Balance URL (API for mobile app)
    path('api/agents/cash_balance/', views.agent_cash_balance, name='agent_cash_balance'),
    
    # Helper API for customers (used by visits)
    path('api/customers/', views.customers_api_list, name='customers_api_list'),
]
