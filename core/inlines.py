"""
Admin inlines for the core application.
Contains inline model configurations for Django admin interface.
"""

from django.contrib import admin
from .models import InvoiceDetail, PriceListDetail


class InvoiceDetailInline(admin.TabularInline):
    """
    Inline for editing invoice details within the invoice master admin page.
    Allows editing invoice line items directly from the invoice page.
    """
    model = InvoiceDetail
    extra = 1
    raw_id_fields = ['item', 'storeID']
    readonly_fields = ['createdAt', 'updatedAt']
    fields = ['item', 'quantity', 'price', 'discountAmount', 'discountPercentage', 
              'taxAmount', 'taxPercentage', 'storeID', 'notes']


class PriceListDetailInline(admin.TabularInline):
    """
    Inline for editing price list details within the price list admin page.
    Allows editing price list items directly from the price list page.
    """
    model = PriceListDetail
    extra = 1
    raw_id_fields = ['item']
    readonly_fields = ['createdAt', 'updatedAt']
    fields = ['item', 'price']
