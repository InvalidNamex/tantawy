from django.urls import path
from . import views

# URLConf
app_name = 'core'

urlpatterns = [
    # ItemsGroup URLs
    path('items-groups/', views.itemsgroup_list, name='itemsgroup_list'),
    path('items-groups/<int:id>/', views.itemsgroup_detail, name='itemsgroup_detail'),
    
    # Item URLs
    path('items/', views.item_list, name='item_list'),
    path('items/<int:id>/', views.item_detail, name='item_detail'),
    path('items/group/<int:group_id>/', views.item_by_group, name='item_by_group'),
    
    # PriceList URLs
    path('price-lists/', views.pricelist_list, name='pricelist_list'),
    path('price-lists/<int:id>/', views.pricelist_detail, name='pricelist_detail'),
    
    # PriceListDetail URLs
    path('price-list-details/', views.pricelistdetail_list, name='pricelistdetail_list'),
    path('price-list-details/pricelist/<int:pricelist_id>/', views.pricelistdetail_by_pricelist, name='pricelistdetail_by_pricelist'),
    
    # StoreGroup URLs
    path('store-groups/', views.storegroup_list, name='storegroup_list'),
    path('store-groups/<int:id>/', views.storegroup_detail, name='storegroup_detail'),
    
    # Store URLs
    path('stores/', views.store_list, name='store_list'),
    path('stores/<int:id>/', views.store_detail, name='store_detail'),
]
