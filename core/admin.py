"""
Django admin configuration for core models.
Provides comprehensive admin interface for all models with proper filtering, search, and inline editing.
"""

from django.contrib import admin
from .models import *
from .inlines import InvoiceDetailInline, PriceListDetailInline


@admin.register(ItemsGroup)
class ItemsGroupAdmin(admin.ModelAdmin):
    """Admin interface for ItemsGroup model with search and filtering capabilities."""
    list_display = ['id', 'itemsGroupName', 'createdAt', 'isDeleted']
    list_filter = ['isDeleted', 'createdAt']
    search_fields = ['itemsGroupName']
    readonly_fields = ['createdAt', 'updatedAt']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('itemsGroupName',)
        }),
        ('Audit Information', {
            'fields': ('createdAt', 'updatedAt', 'deletedAt', 'isDeleted'),
            'classes': ('collapse',)
        }),
        ('User Tracking', {
            'fields': ('createdBy', 'updatedBy', 'deletedBy'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Admin interface for Item model with comprehensive filtering and search."""
    list_display = ['id', 'itemName', 'itemGroupId', 'isUsed', 'isTax', 'isDeleted']
    list_filter = ['isDeleted', 'isUsed', 'isTax', 'itemGroupId']
    search_fields = ['itemName', 'barcode', 'subUnitBarCode', 'smallUnitBarCode']
    readonly_fields = ['createdAt', 'updatedAt']
    raw_id_fields = ['itemGroupId']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('itemGroupId', 'itemName', 'itemImage', 'barcode', 'sign')
        }),
        ('Item Properties', {
            'fields': ('isUsed', 'isTax')
        }),
        ('Unit Information', {
            'fields': ('mainUnitName', 'subUnitName', 'smallUnitName', 
                      'mainUnitPack', 'subUnitPack', 'subUnitBarCode', 'smallUnitBarCode')
        }),
        ('Audit Information', {
            'fields': ('createdAt', 'updatedAt', 'deletedAt', 'isDeleted'),
            'classes': ('collapse',)
        }),
        ('User Tracking', {
            'fields': ('createdBy', 'updatedBy', 'deletedBy'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    """Admin interface for PriceList model with inline price list details."""
    list_display = ['id', 'priceListName', 'createdAt', 'isDeleted']
    list_filter = ['isDeleted', 'createdAt']
    search_fields = ['priceListName']
    readonly_fields = ['createdAt', 'updatedAt']
    inlines = [PriceListDetailInline]

@admin.register(PriceListDetail)
class PriceListDetailAdmin(admin.ModelAdmin):
    """Admin interface for PriceListDetail model with related object information."""
    list_display = ['id', 'priceList', 'item', 'price', 'isDeleted']
    list_filter = ['isDeleted', 'priceList']
    search_fields = ['priceList__priceListName', 'item__itemName']
    readonly_fields = ['createdAt', 'updatedAt']
    raw_id_fields = ['priceList', 'item']

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

@admin.register(CustomerVendor)
class CustomerVendorAdmin(admin.ModelAdmin):
    list_display = ['id', 'customerVendorName', 'type', 'phone_one', 'isDeleted']
    list_filter = ['isDeleted', 'type', 'createdAt']
    search_fields = ['customerVendorName', 'phone_one', 'phone_two']
    readonly_fields = ['createdAt', 'updatedAt']
    
    def get_type_display(self, obj):
        return obj.get_type_display()
    get_type_display.short_description = 'Type'

@admin.register(InvoiceMaster)
class InvoiceMasterAdmin(admin.ModelAdmin):
    """Admin interface for InvoiceMaster model with comprehensive filtering and inline invoice details."""
    list_display = ['id', 'get_invoice_type_display', 'customerOrVendorID', 'storeID', 
                   'get_status_display', 'netTotal', 'createdAt', 'isDeleted']
    list_filter = ['isDeleted', 'invoiceType', 'status', 'paymentType', 'returnStatus', 'createdAt']
    search_fields = ['customerOrVendorID__customerVendorName', 'storeID__storeName', 'notes']
    readonly_fields = ['createdAt', 'updatedAt']
    raw_id_fields = ['customerOrVendorID', 'storeID', 'originalInvoiceID']
    inlines = [InvoiceDetailInline]
    
    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoiceType', 'customerOrVendorID', 'storeID', 'originalInvoiceID', 'notes')
        }),
        ('Financial Details', {
            'fields': ('discountAmount', 'discountPercentage', 'taxAmount', 'taxPercentage', 'netTotal')
        }),
        ('Payment Information', {
            'fields': ('paymentType', 'status', 'totalPaid', 'returnStatus')
        }),
        ('Audit Information', {
            'fields': ('createdAt', 'updatedAt', 'deletedAt', 'isDeleted'),
            'classes': ('collapse',)
        }),
        ('User Tracking', {
            'fields': ('createdBy', 'updatedBy', 'deletedBy'),
            'classes': ('collapse',)
        }),
    )
    
    def get_invoice_type_display(self, obj):
        """Display human-readable invoice type."""
        return obj.get_invoiceType_display()
    get_invoice_type_display.short_description = 'Invoice Type'
    
    def get_status_display(self, obj):
        """Display human-readable status."""
        return obj.get_status_display()
    get_status_display.short_description = 'Status'

@admin.register(InvoiceDetail)
class InvoiceDetailAdmin(admin.ModelAdmin):
    """Admin interface for InvoiceDetail model with related object filtering."""
    list_display = ['id', 'invoiceMasterID', 'item', 'quantity', 'price', 'storeID', 'isDeleted']
    list_filter = ['isDeleted', 'invoiceMasterID__invoiceType', 'storeID', 'createdAt']
    search_fields = ['item__itemName', 'invoiceMasterID__id', 'notes']
    readonly_fields = ['createdAt', 'updatedAt']
    raw_id_fields = ['item', 'invoiceMasterID', 'storeID']
    
    fieldsets = (
        ('Line Item Information', {
            'fields': ('invoiceMasterID', 'item', 'quantity', 'price', 'storeID', 'notes')
        }),
        ('Discounts and Taxes', {
            'fields': ('discountAmount', 'discountPercentage', 'taxAmount', 'taxPercentage')
        }),
        ('Audit Information', {
            'fields': ('createdAt', 'updatedAt', 'deletedAt', 'isDeleted'),
            'classes': ('collapse',)
        }),
        ('User Tracking', {
            'fields': ('createdBy', 'updatedBy', 'deletedBy'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Admin interface for Account model with comprehensive management capabilities."""
    list_display = ['id', 'accountName', 'accountGroup', 'sign', 'createdAt', 'isDeleted']
    list_filter = ['isDeleted', 'accountGroup', 'createdAt']
    search_fields = ['accountName', 'sign']
    readonly_fields = ['createdAt', 'updatedAt']
    ordering = ['accountName']
    
    fieldsets = (
        ('Account Information', {
            'fields': ('accountName', 'accountGroup', 'sign')
        }),
        ('Audit Information', {
            'fields': ('createdAt', 'updatedAt', 'deletedAt', 'isDeleted'),
            'classes': ('collapse',)
        }),
        ('User Tracking', {
            'fields': ('createdBy', 'updatedBy', 'deletedBy'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin interface for Transaction model with comprehensive filtering and management."""
    list_display = ['id', 'accountID', 'amount', 'type', 'get_type_display', 'customerVendorID', 'invoiceID', 'createdAt', 'isDeleted']
    list_filter = ['isDeleted', 'type', 'accountID', 'customerVendorID', 'createdAt']
    search_fields = ['accountID__accountName', 'customerVendorID__customerVendorName', 'notes', 'invoiceID__id']
    readonly_fields = ['createdAt', 'updatedAt']
    raw_id_fields = ['accountID', 'customerVendorID', 'invoiceID']
    ordering = ['-createdAt']
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('accountID', 'amount', 'type', 'notes')
        }),
        ('Related Records', {
            'fields': ('customerVendorID', 'invoiceID')
        }),
        ('Audit Information', {
            'fields': ('createdAt', 'updatedAt', 'deletedAt', 'isDeleted'),
            'classes': ('collapse',)
        }),
        ('User Tracking', {
            'fields': ('createdBy', 'updatedBy', 'deletedBy'),
            'classes': ('collapse',)
        }),
    )
    
    def get_type_display(self, obj):
        """Display human-readable transaction type."""
        return obj.get_type_display() if obj.type else '-'
    get_type_display.short_description = 'Transaction Type'
