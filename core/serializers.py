"""
Django REST Framework serializers for core models.
Provides comprehensive serialization with nested relationships and display fields.
"""

from rest_framework import serializers
from core.models import *


class ItemsGroupSerializer(serializers.ModelSerializer):
    """Serializer for ItemsGroup model with all audit fields."""
    
    class Meta:
        model = ItemsGroup
        fields = ['id', 'itemsGroupName', 'createdAt', 'updatedAt', 'deletedAt', 
                 'createdBy', 'updatedBy', 'deletedBy', 'isDeleted']
        read_only_fields = ['createdAt', 'updatedAt']


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item model with group relationship and detailed fields."""
    
    group_name = serializers.CharField(source='itemGroupId.itemsGroupName', read_only=True)
    
    class Meta:
        model = Item
        fields = ['id', 'itemGroupId', 'group_name', 'itemName', 'itemImage', 'barcode', 'sign', 
                 'isUsed', 'isTax', 'mainUnitName', 'subUnitName', 'smallUnitName', 'mainUnitPack', 
                 'subUnitPack', 'subUnitBarCode', 'smallUnitBarCode', 'createdAt', 'updatedAt', 
                 'deletedAt', 'createdBy', 'updatedBy', 'deletedBy', 'isDeleted']
        read_only_fields = ['createdAt', 'updatedAt']


class PriceListSerializer(serializers.ModelSerializer):
    """Serializer for PriceList model with audit fields."""
    
    class Meta:
        model = PriceList
        fields = ['id', 'priceListName', 'createdAt', 'updatedAt', 'deletedAt', 
                 'createdBy', 'updatedBy', 'deletedBy', 'isDeleted']
        read_only_fields = ['createdAt', 'updatedAt']


class PriceListDetailSerializer(serializers.ModelSerializer):
    """Serializer for PriceListDetail model with related object names."""
    
    price_list_name = serializers.CharField(source='priceList.priceListName', read_only=True)
    item_name = serializers.CharField(source='item.itemName', read_only=True)
    
    class Meta:
        model = PriceListDetail
        fields = ['id', 'priceList', 'price_list_name', 'item', 'item_name', 'price', 
                 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 
                 'deletedBy', 'isDeleted']
        read_only_fields = ['createdAt', 'updatedAt']


class StoreGroupSerializer(serializers.ModelSerializer):
    """Serializer for StoreGroup model with audit fields."""
    
    class Meta:
        model = StoreGroup
        fields = ['id', 'storeGroupName', 'createdAt', 'updatedAt', 'deletedAt', 
                 'createdBy', 'updatedBy', 'deletedBy', 'isDeleted']
        read_only_fields = ['createdAt', 'updatedAt']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'storeName', 'storeGroup', 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 'deletedBy', 'isDeleted']

class CustomerVendorSerializer(serializers.ModelSerializer):
    """Serializer for CustomerVendor model with type display and comprehensive fields."""
    
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = CustomerVendor
        fields = ['id', 'customerVendorName', 'phone_one', 'phone_two', 'type', 'type_display', 
                 'notes', 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 
                 'deletedBy', 'isDeleted']
        read_only_fields = ['createdAt', 'updatedAt']


class InvoiceDetailSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceDetail model with related object information."""
    
    item_name = serializers.CharField(source='item.itemName', read_only=True)
    store_name = serializers.CharField(source='storeID.storeName', read_only=True)
    
    class Meta:
        model = InvoiceDetail
        fields = ['id', 'item', 'item_name', 'quantity', 'price', 'notes', 'invoiceMasterID', 
                 'storeID', 'store_name', 'discountAmount', 'discountPercentage', 'taxAmount', 
                 'taxPercentage', 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 
                 'updatedBy', 'deletedBy', 'isDeleted']
        read_only_fields = ['createdAt', 'updatedAt']


class InvoiceMasterSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for InvoiceMaster model with nested invoice details.
    Includes all choice field displays and related object information.
    """
    
    invoice_type_display = serializers.CharField(source='get_invoiceType_display', read_only=True)
    payment_type_display = serializers.CharField(source='get_paymentType_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    return_status_display = serializers.CharField(source='get_returnStatus_display', read_only=True)
    customer_vendor_name = serializers.CharField(source='customerOrVendorID.customerVendorName', read_only=True)
    store_name = serializers.CharField(source='storeID.storeName', read_only=True)
    invoice_details = InvoiceDetailSerializer(source='invoicedetail_set', many=True, read_only=True)
    
    class Meta:
        model = InvoiceMaster
        fields = ['id', 'customerOrVendorID', 'customer_vendor_name', 'storeID', 'store_name', 
                 'invoiceType', 'invoice_type_display', 'notes', 'discountAmount', 
                 'discountPercentage', 'taxAmount', 'taxPercentage', 'netTotal', 'paymentType', 
                 'payment_type_display', 'status', 'status_display', 'totalPaid', 'returnStatus', 
                 'return_status_display', 'originalInvoiceID', 'invoice_details', 'createdAt', 
                 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 'deletedBy', 'isDeleted']
        read_only_fields = ['createdAt', 'updatedAt']

class CustomerVendorSerializer(serializers.ModelSerializer):
    """Serializer for CustomerVendor model"""
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = CustomerVendor
        fields = ['id', 'customerVendorName', 'phone_one', 'phone_two', 'type', 'type_display', 
                 'notes', 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 
                 'deletedBy', 'isDeleted']

class InvoiceDetailSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceDetail model"""
    item_name = serializers.CharField(source='item.itemName', read_only=True)
    store_name = serializers.CharField(source='storeID.storeName', read_only=True)
    
    class Meta:
        model = InvoiceDetail
        fields = ['id', 'item', 'item_name', 'quantity', 'price', 'notes', 'invoiceMasterID', 
                 'storeID', 'store_name', 'discountAmount', 'discountPercentage', 'taxAmount', 
                 'taxPercentage', 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 
                 'deletedBy', 'isDeleted']

class InvoiceMasterSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceMaster model"""
    invoiceType_display = serializers.CharField(source='get_invoiceType_display', read_only=True)
    paymentType_display = serializers.CharField(source='get_paymentType_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    returnStatus_display = serializers.CharField(source='get_returnStatus_display', read_only=True)
    customer_vendor_name = serializers.CharField(source='customerOrVendorID.customerVendorName', read_only=True)
    store_name = serializers.CharField(source='storeID.storeName', read_only=True)
    agent_name = serializers.CharField(source='agentID.agentName', read_only=True)
    original_invoice_type = serializers.CharField(source='originalInvoiceID.get_invoiceType_display', read_only=True)
    
    # Nested invoice details
    invoice_details = InvoiceDetailSerializer(source='invoicedetail_set', many=True, read_only=True)
    
    class Meta:
        model = InvoiceMaster
        fields = ['id', 'customerOrVendorID', 'customer_vendor_name', 'storeID', 'store_name', 
                 'agentID', 'agent_name', 'invoiceType', 'invoiceType_display', 'notes', 
                 'discountAmount', 'discountPercentage', 'taxAmount', 'taxPercentage', 'netTotal', 
                 'paymentType', 'paymentType_display', 'status', 'status_display', 'totalPaid', 
                 'returnStatus', 'returnStatus_display', 'originalInvoiceID', 'original_invoice_type', 
                 'invoice_details', 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 
                 'deletedBy', 'isDeleted']


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for Account model with user information.
    Provides comprehensive account management for the accounting system.
    """
    
    created_by_name = serializers.CharField(source='createdBy.username', read_only=True)
    updated_by_name = serializers.CharField(source='updatedBy.username', read_only=True)
    
    class Meta:
        model = Account
        fields = ['id', 'accountName', 'accountGroup', 'sign', 'created_by_name', 
                 'updated_by_name', 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 
                 'updatedBy', 'deletedBy', 'isDeleted']
        read_only_fields = ['createdAt', 'updatedAt']


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction model with related object information.
    Includes display names for choice fields and foreign key relationships.
    """
    
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    account_name = serializers.CharField(source='accountID.accountName', read_only=True)
    customer_vendor_name = serializers.CharField(source='customerVendorID.customerVendorName', read_only=True)
    invoice_type_display = serializers.CharField(source='invoiceID.get_invoiceType_display', read_only=True)
    created_by_name = serializers.CharField(source='createdBy.username', read_only=True)
    updated_by_name = serializers.CharField(source='updatedBy.username', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'accountID', 'account_name', 'amount', 'notes', 'type', 'type_display',
                 'customerVendorID', 'customer_vendor_name', 'invoiceID', 'invoice_type_display',
                 'created_by_name', 'updated_by_name', 'createdAt', 'updatedAt', 'deletedAt', 
                 'createdBy', 'updatedBy', 'deletedBy', 'isDeleted']
        read_only_fields = ['createdAt', 'updatedAt']


class AgentSerializer(serializers.ModelSerializer):
    """
    Serializer for Agent model with independent authentication.
    Handles password hashing and validation for mobile app authentication.
    """
    
    password = serializers.CharField(source='agentPassword', write_only=True, min_length=6,
                                   help_text="Password for agent authentication (minimum 6 characters)")
    created_by_name = serializers.CharField(source='createdBy.username', read_only=True)
    updated_by_name = serializers.CharField(source='updatedBy.username', read_only=True)
    
    class Meta:
        model = Agent
        fields = ['id', 'agentName', 'agentUsername', 'agentPhone', 
                 'isActive', 'password', 'created_by_name', 'updated_by_name',
                 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 
                 'deletedBy', 'isDeleted']
        read_only_fields = ['createdAt', 'updatedAt']
        extra_kwargs = {
            'agentPassword': {'write_only': True},
            'agentUsername': {'help_text': 'Unique username for agent login'},
            'agentPhone': {'help_text': 'Agent phone number'},
            'isActive': {'help_text': 'Whether the agent can login'},
        }
    
    def create(self, validated_data):
        """Create a new agent with properly hashed password."""
        password = validated_data.pop('agentPassword', None)
        agent = Agent.objects.create(**validated_data)
        if password:
            agent.set_password(password)
            agent.save()
        return agent
    
    def update(self, instance, validated_data):
        """Update agent with password hashing if password is provided."""
        password = validated_data.pop('agentPassword', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
    
    def validate_agentUsername(self, value):
        """Validate that username is unique."""
        if Agent.objects.filter(agentUsername=value, isDeleted=False).exists():
            if not self.instance or self.instance.agentUsername != value:
                raise serializers.ValidationError("This username is already taken.")
        return value


class VisitSerializer(serializers.ModelSerializer):
    """Serializer for Visit model with related object information."""
    
    agent_name = serializers.CharField(source='agentID.agentName', read_only=True)
    customer_vendor_name = serializers.CharField(source='customerVendor.customerVendorName', read_only=True)
    trans_type_display = serializers.CharField(source='get_transType_display', read_only=True)
    
    class Meta:
        model = Visit
        fields = ['id', 'transType', 'trans_type_display', 'customerVendor', 'customer_vendor_name', 
                 'date', 'latitude', 'longitude', 'agentID', 'agent_name', 'notes', 
                 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 
                 'deletedBy', 'isDeleted']
        read_only_fields = ['createdAt', 'updatedAt']
    
    def validate(self, data):
        """Custom validation for visit data."""
        # For pay vouchers (type 4), customerVendor can be null
        if data.get('transType') != 4 and not data.get('customerVendor'):
            raise serializers.ValidationError("Customer/Vendor is required for this transaction type.")
        return data


class VisitPlanSerializer(serializers.ModelSerializer):
    """Serializer for VisitPlan model with related object information."""
    
    agent_name = serializers.CharField(source='agentID.agentName', read_only=True)
    customer_count = serializers.SerializerMethodField()
    customer_details = serializers.SerializerMethodField()
    
    class Meta:
        model = VisitPlan
        fields = ['id', 'agentID', 'agent_name', 'dateFrom', 'dateTo', 'customers', 
                 'customer_count', 'customer_details', 'notes', 'isActive',
                 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 
                 'deletedBy', 'isDeleted']
        read_only_fields = ['createdAt', 'updatedAt']
    
    def get_customer_count(self, obj):
        """Return the number of customers in the plan."""
        if obj.customers and isinstance(obj.customers, list):
            return len(obj.customers)
        return 0
    
    def get_customer_details(self, obj):
        """Return list of customer objects with id and name."""
        if not obj.customers or not isinstance(obj.customers, list):
            return []
        
        try:
            customer_ids = obj.customers
            customers = CustomerVendor.objects.filter(id__in=customer_ids, isDeleted=False)
            return [
                {
                    'id': c.id,
                    'name': c.customerVendorName,
                    'phone_one': c.phone_one,
                    'phone_two': c.phone_two,
                    'type': c.type,
                }
                for c in customers
            ]
        except Exception:
            return []
    
    def validate_customers(self, value):
        """Validate that customers is a list of integers."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Customers must be a list of customer IDs.")
        
        if not all(isinstance(item, int) for item in value):
            raise serializers.ValidationError("All customer IDs must be integers.")
        
        # Validate that all customer IDs exist
        existing_ids = CustomerVendor.objects.filter(
            id__in=value, 
            isDeleted=False
        ).values_list('id', flat=True)
        
        invalid_ids = set(value) - set(existing_ids)
        if invalid_ids:
            raise serializers.ValidationError(
                f"Invalid customer IDs: {', '.join(map(str, invalid_ids))}"
            )
        
        return value
    
    def validate(self, data):
        """Custom validation for visit plan data."""
        date_from = data.get('dateFrom')
        date_to = data.get('dateTo')
        
        if date_from and date_to and date_from > date_to:
            raise serializers.ValidationError("dateFrom must be before or equal to dateTo.")
        
        return data
