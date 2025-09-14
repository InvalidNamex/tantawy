from django.contrib import admin
from .models import *

@admin.register(ItemsGroup)
class ItemsGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'itemsGroupName', 'createdAt', 'isDeleted']
    list_filter = ['isDeleted', 'createdAt']
    search_fields = ['itemsGroupName']
    readonly_fields = ['createdAt', 'updatedAt']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'itemName', 'itemGroupId', 'isUsed', 'isTax', 'isDeleted']
    list_filter = ['isDeleted', 'isUsed', 'isTax', 'itemGroupId']
    search_fields = ['itemName', 'barcode']
    readonly_fields = ['createdAt', 'updatedAt']

@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    list_display = ['id', 'priceListName', 'createdAt', 'isDeleted']
    list_filter = ['isDeleted', 'createdAt']
    search_fields = ['priceListName']
    readonly_fields = ['createdAt', 'updatedAt']

@admin.register(PriceListDetail)
class PriceListDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'priceList', 'item', 'price', 'isDeleted']
    list_filter = ['isDeleted', 'priceList']
    search_fields = ['priceList__priceListName', 'item__itemName']
    readonly_fields = ['createdAt', 'updatedAt']

@admin.register(StoreGroup)
class StoreGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'storeGroupName', 'createdAt', 'isDeleted']
    list_filter = ['isDeleted', 'createdAt']
    search_fields = ['storeGroupName']
    readonly_fields = ['createdAt', 'updatedAt']

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'storeName', 'storeGroup', 'isDeleted']
    list_filter = ['isDeleted', 'storeGroup']
    search_fields = ['storeName', 'storeGroup']
    readonly_fields = ['createdAt', 'updatedAt']
