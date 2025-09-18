from django.urls import path
from . import views

# URLConf
app_name = 'core'

urlpatterns = [
    # ItemsGroup URLs
    path('items-groups/', views.itemsgroup_list, name='itemsgroup_list'),
    path('items-groups/<int:id>/', views.itemsgroup_detail, name='itemsgroup_detail'),
    
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
    
    # PriceList URLs (API)
    path('price-lists/', views.pricelist_list, name='pricelist_list'),
    path('price-lists/<int:id>/', views.pricelist_detail, name='pricelist_detail'),
    
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
    
    # PriceListDetail URLs
    path('price-list-details/', views.pricelistdetail_list, name='pricelistdetail_list'),
    path('price-list-details/pricelist/<int:pricelist_id>/', views.pricelistdetail_by_pricelist, name='pricelistdetail_by_pricelist'),
    
    # StoreGroup URLs
    path('store-groups/', views.storegroup_list, name='storegroup_list'),
    path('store-groups/<int:id>/', views.storegroup_detail, name='storegroup_detail'),
    
    # Store URLs
    path('stores/', views.store_list, name='store_list'),
    path('stores/<int:id>/', views.store_detail, name='store_detail'),
    
    # CustomerVendor URLs
    path('customers-vendors/', views.customervendor_list, name='customervendor_list'),
    path('customers-vendors/<int:id>/', views.customervendor_detail, name='customervendor_detail'),
    
    # InvoiceMaster URLs
    path('invoices/', views.invoicemaster_list, name='invoicemaster_list'),
    path('invoices/<int:id>/', views.invoicemaster_detail, name='invoicemaster_detail'),
    
    # InvoiceDetail URLs
    path('invoice-details/', views.invoicedetail_list, name='invoicedetail_list'),
    path('invoice-details/<int:id>/', views.invoicedetail_detail, name='invoicedetail_detail'),
    
    # Stock URLs
    path('stock/', views.item_stock, name='item_stock'),
    
    # Account URLs
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/<int:id>/', views.account_detail, name='account_detail'),
    path('accounts/create/', views.account_create, name='account_create'),
    
    # Transaction URLs
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/<int:id>/', views.transaction_detail, name='transaction_detail'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    
    # Item URLs (API)
    path('api/items/', views.item_list, name='item_list'),
    path('api/items/<int:id>/', views.item_detail, name='item_detail'),
    path('api/items/group/<int:group_id>/', views.item_by_group, name='item_by_group'),
]
