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
                   'agentID', 'get_status_display', 'netTotal', 'createdAt', 'isDeleted']
    list_filter = ['isDeleted', 'invoiceType', 'status', 'paymentType', 'returnStatus', 'agentID', 'createdAt']
    search_fields = ['customerOrVendorID__customerVendorName', 'storeID__storeName', 'agentID__agentName', 'notes']
    readonly_fields = ['createdAt', 'updatedAt']
    raw_id_fields = ['customerOrVendorID', 'storeID', 'agentID', 'originalInvoiceID']
    inlines = [InvoiceDetailInline]
    
    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoiceType', 'customerOrVendorID', 'storeID', 'agentID', 'originalInvoiceID', 'notes')
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


from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


class AgentCreationForm(forms.ModelForm):
    """A form for creating new agents with password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Agent
        fields = ('agentName', 'agentUsername', 'agentPhone', 'isActive')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        agent = super().save(commit=False)
        agent.set_password(self.cleaned_data["password1"])
        if commit:
            agent.save()
        return agent


class AgentChangeForm(forms.ModelForm):
    """A form for updating agents. Includes all the fields on
    the agent, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField(label="Password", 
                                       help_text="Raw passwords are not stored, so there is no way to see this "
                                               "agent's password, but you can change the password using "
                                               "<a href=\"../password/\">this form</a>.")

    class Meta:
        model = Agent
        fields = ('agentName', 'agentUsername', 'agentPhone', 'isActive', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['password'].initial = self.instance.agentPassword

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get("password")


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    """Admin interface for Agent model with independent authentication."""
    form = AgentChangeForm
    add_form = AgentCreationForm
    
    list_display = ['id', 'agentName', 'agentUsername', 'isActive', 'createdAt', 'isDeleted']
    list_filter = ['isDeleted', 'isActive', 'createdAt']
    search_fields = ['agentName', 'agentUsername']
    readonly_fields = ['createdAt', 'updatedAt']
    ordering = ['agentName']
    
    fieldsets = (
        ('Agent Information', {
            'fields': ('agentName', 'agentUsername', 'agentPhone', 'isActive')
        }),
        ('Authentication', {
            'fields': ('password',),
            'classes': ('collapse',),
            'description': 'Password is automatically hashed. Use the change password form to update.'
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
    
    add_fieldsets = (
        ('Agent Information', {
            'fields': ('agentName', 'agentUsername', 'agentPhone', 'isActive')
        }),
        ('Authentication', {
            'fields': ('password1', 'password2'),
            'description': 'Enter a secure password for the agent.'
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during agent creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)
    
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        """Override save to handle password hashing and audit fields."""
        if not change:  # Creating new agent
            obj.createdBy = request.user
        obj.updatedBy = request.user
        super().save_model(request, obj, form, change)
