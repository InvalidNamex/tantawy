"""
Core models for the DRF project.
Contains all database models with audit fields and proper relationships.
"""

from django.db import models
from django.contrib.auth.models import User
from .constants import *


class BaseModel(models.Model):
    """
    Base model with common audit fields for all models.
    Provides tracking of creation, updates, and deletion with user information.
    """
    createdAt = models.DateTimeField(auto_now_add=True, help_text="Timestamp when record was created")
    updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True, help_text="Timestamp when record was last updated")
    deletedAt = models.DateTimeField(null=True, blank=True, help_text="Timestamp when record was soft deleted")
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_created', 
                                 null=True, blank=True, help_text="User who created this record")
    updatedBy = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_updated', 
                                 null=True, blank=True, help_text="User who last updated this record")
    deletedBy = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_deleted', 
                                 null=True, blank=True, help_text="User who soft deleted this record")
    isDeleted = models.BooleanField(default=False, help_text="Indicates if record is soft deleted")
    
    class Meta:
        abstract = True

class ItemsGroup(BaseModel):
    itemsGroupName = models.CharField(max_length=255)
    
    def __str__(self):
        return self.itemsGroupName
    
    class Meta:
        ordering = ['itemsGroupName']
        db_table = 'itemsGroups'

class Item(BaseModel):
    itemGroupId = models.ForeignKey(ItemsGroup, on_delete=models.PROTECT, blank=True, null=True)
    itemName = models.CharField(max_length=255)
    itemImage = models.CharField(max_length=255, blank=True, null=True)  # Allow NULL for optional image
    barcode = models.CharField(max_length=255, blank=True, null=True)    # Allow NULL for optional barcode
    sign = models.CharField(max_length=255, blank=True, null=True)       # Allow NULL for optional sign
    isUsed = models.BooleanField(default=False)
    isTax = models.BooleanField(default=False)
    mainUnitName = models.CharField(max_length=255, blank=True, null=True)      # Allow NULL for optional unit names
    subUnitName = models.CharField(max_length=255, blank=True, null=True)       # Allow NULL for optional unit names
    smallUnitName = models.CharField(max_length=255, blank=True, null=True)     # Allow NULL for optional unit names
    mainUnitPack = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subUnitPack = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subUnitBarCode = models.CharField(max_length=255, blank=True, null=True)    # Allow NULL for optional barcode
    smallUnitBarCode = models.CharField(max_length=255, blank=True, null=True)  # Allow NULL for optional barcode
    
    def get_stock_by_store(self, store_id=None):
        """Calculate stock for this item in a specific store or all stores"""
        from django.db.models import Sum, Case, When, DecimalField
        
        queryset = self.invoicedetail_set.select_related('invoiceMasterID').filter(
            isDeleted=False,
            invoiceMasterID__isDeleted=False
        )
        
        if store_id:
            queryset = queryset.filter(storeID=store_id)
        
        # Calculate purchases (invoice type 1) and sales (invoice type 2)
        aggregation = queryset.aggregate(
            purchases=Sum(
                Case(
                    When(invoiceMasterID__invoiceType=1, then='quantity'),
                    default=0,
                    output_field=DecimalField(max_digits=10, decimal_places=3)
                )
            ),
            sales=Sum(
                Case(
                    When(invoiceMasterID__invoiceType=2, then='quantity'),
                    default=0,
                    output_field=DecimalField(max_digits=10, decimal_places=3)
                )
            )
        )
        
        purchases = aggregation.get('purchases') or 0
        sales = aggregation.get('sales') or 0
        return purchases - sales
    
    def __str__(self):
        return self.itemName
    
    class Meta:
        ordering = ['itemName']
        db_table = 'items'

class PriceList(BaseModel):
    priceListName = models.CharField(max_length=255)
    
    def __str__(self):
        return self.priceListName
    
    class Meta:
        ordering = ['priceListName']
        db_table = 'priceLists'

class PriceListDetail(BaseModel):
    priceList = models.ForeignKey(PriceList, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.priceList.priceListName} - {self.item.itemName}"
    
    class Meta:
        ordering = ['priceList', 'item']
        db_table = 'priceListsDetails'

class StoreGroup(BaseModel):
    storeGroupName = models.CharField(max_length=255)
    
    def __str__(self):
        return self.storeGroupName
    
    class Meta:
        ordering = ['storeGroupName']
        db_table = 'storeGroups'

class Store(BaseModel):
    storeName = models.CharField(max_length=255)
    storeGroup = models.CharField(max_length=255, blank=True, null=True)  # Allow NULL for optional store group
    
    def __str__(self):
        return self.storeName
    
    class Meta:
        ordering = ['storeName']
        db_table = 'stores'

class CustomerVendor(BaseModel):
    """
    Customer and Vendor model - type field determines if customer, vendor, or both.
    Supports tracking of business relationships with proper contact information.
    """
    
    customerVendorName = models.TextField(help_text="Name of the customer or vendor")
    phone_one = models.CharField(max_length=255, blank=True, null=True, help_text="Primary phone number")
    phone_two = models.CharField(max_length=255, blank=True, null=True, help_text="Secondary phone number")
    type = models.SmallIntegerField(choices=CUSTOMER_VENDOR_TYPE_CHOICES, default=1, 
                                   help_text="Type: 1=Customer, 2=Vendor, 3=Both")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes or comments")
    
    def __str__(self):
        return f"{self.customerVendorName} ({self.get_type_display()})"
    
    class Meta:
        ordering = ['customerVendorName']
        db_table = 'customerVendor'
        verbose_name = "Customer/Vendor"
        verbose_name_plural = "Customers/Vendors"

class InvoiceMaster(BaseModel):
    """
    Invoice Master table for all invoice types (purchases, sales, returns).
    Central table for invoice management with comprehensive tracking of financial data.
    """
    
    customerOrVendorID = models.ForeignKey(CustomerVendor, on_delete=models.PROTECT, null=True, blank=True,
                                          help_text="Associated customer or vendor")
    storeID = models.ForeignKey('Store', on_delete=models.PROTECT, null=True, blank=True,
                               help_text="Store where invoice was processed")
    invoiceType = models.IntegerField(choices=INVOICE_TYPE_CHOICES, 
                                     help_text="Type: 1=Purchases, 2=Sales, 3=Return Purchases, 4=Return Sales")
    notes = models.TextField(blank=True, null=True, help_text="Invoice notes or comments")
    discountAmount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                        help_text="Fixed discount amount")
    discountPercentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                           help_text="Percentage discount (0-100)")
    taxAmount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                   help_text="Fixed tax amount")
    taxPercentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                       help_text="Tax percentage (0-100)")
    netTotal = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                  help_text="Final total amount after discounts and taxes")
    paymentType = models.SmallIntegerField(choices=PAYMENT_TYPE_CHOICES, default=PAYMENT_TYPE_CASH,
                                          help_text="Payment method: 1=Cash, 2=Visa, 3=Partial/Deferred")
    status = models.SmallIntegerField(choices=INVOICE_STATUS_CHOICES, default=STATUS_PAID,
                                     help_text="Payment status: 0=Paid, 1=Unpaid, 2=Partially Paid")
    totalPaid = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                   help_text="Amount actually paid")
    returnStatus = models.SmallIntegerField(choices=RETURN_STATUS_CHOICES, default=RETURN_STATUS_NOT_RETURNED,
                                           help_text="Return status: 0=Not Returned, 1=Partially Returned, 2=Fully Returned")
    originalInvoiceID = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,
                                         help_text="Reference to original invoice for return invoices")
    
    def __str__(self):
        return f"Invoice {self.id} - {self.get_invoiceType_display()}"
    
    class Meta:
        ordering = ['-createdAt']
        db_table = 'invoiceMaster'
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

class InvoiceDetail(BaseModel):
    """
    Invoice Detail table for line items.
    Contains individual line items for each invoice with quantity, pricing, and tax information.
    """
    
    item = models.ForeignKey('Item', on_delete=models.PROTECT, help_text="Item being invoiced")
    quantity = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,
                                  help_text="Quantity of items")
    price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                               help_text="Unit price per item")
    notes = models.TextField(blank=True, null=True, help_text="Line item notes")
    invoiceMasterID = models.ForeignKey(InvoiceMaster, on_delete=models.CASCADE, 
                                       help_text="Associated invoice master record")
    storeID = models.ForeignKey('Store', on_delete=models.PROTECT, null=True, blank=True,
                               help_text="Store for this line item")
    discountAmount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                        help_text="Line item discount amount")
    discountPercentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                           help_text="Line item discount percentage")
    taxAmount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                   help_text="Line item tax amount")
    taxPercentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                       help_text="Line item tax percentage")
    
    def __str__(self):
        return f"Invoice {self.invoiceMasterID.id} - {self.item.itemName}"
    
    class Meta:
        ordering = ['invoiceMasterID', 'item']
        db_table = 'invoiceDetail'
        verbose_name = "Invoice Detail"
        verbose_name_plural = "Invoice Details"


class Account(BaseModel):
    """
    Accounts model for financial account management.
    Represents chart of accounts with optional account grouping.
    """
    
    accountName = models.TextField(help_text="Name of the account")
    accountGroup = models.BigIntegerField(null=True, blank=True, 
                                         help_text="Account group ID (references cost center)")
    sign = models.BigIntegerField(unique=True, null=True, blank=True,
                                 help_text="Unique sign/code for the account")
    
    def __str__(self):
        return f"{self.accountName} ({self.sign})" if self.sign else self.accountName
    
    class Meta:
        ordering = ['accountName']
        db_table = 'accounts'
        verbose_name = "Account"
        verbose_name_plural = "Accounts"


class Transaction(BaseModel):
    """
    Transactions model for recording financial transactions.
    Links accounts with customer/vendor activities and invoices.
    """
    
    accountID = models.ForeignKey(Account, on_delete=models.PROTECT, 
                                 help_text="Associated account")
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,
                                help_text="Transaction amount")
    notes = models.TextField(blank=True, null=True, help_text="Transaction notes")
    type = models.SmallIntegerField(choices=TRANSACTION_TYPE_CHOICES, null=True, blank=True,
                                   help_text="Transaction type: 1=Purchase, 2=Sales, 3=Return Purchase, 4=Return Sales")
    customerVendorID = models.ForeignKey(CustomerVendor, on_delete=models.CASCADE, null=True, blank=True,
                                        help_text="Associated customer or vendor")
    invoiceID = models.ForeignKey(InvoiceMaster, on_delete=models.CASCADE, null=True, blank=True,
                                 help_text="Associated invoice")
    
    def __str__(self):
        return f"Transaction {self.id} - {self.accountID.accountName} ({self.amount})"
    
    class Meta:
        ordering = ['-createdAt']
        db_table = 'transactions'
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
