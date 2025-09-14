from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    """Base model with common fields for all models"""
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_created', null=True, blank=True)
    updatedBy = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_updated', null=True, blank=True)
    deletedBy = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_deleted', null=True, blank=True)
    isDeleted = models.BooleanField(default=False)
    
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
    itemGroupId = models.ForeignKey(ItemsGroup, on_delete=models.PROTECT)
    itemName = models.CharField(max_length=255)
    itemImage = models.CharField(max_length=255, blank=True)
    barcode = models.CharField(max_length=255, blank=True)
    sign = models.CharField(max_length=255, blank=True)
    isUsed = models.BooleanField(default=False)
    isTax = models.BooleanField(default=False)
    mainUnitName = models.CharField(max_length=255, blank=True)
    subUnitName = models.CharField(max_length=255, blank=True)
    smallUnitName = models.CharField(max_length=255, blank=True)  # Fixed duplicate field name
    mainUnitPack = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subUnitPack = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subUnitBarCode = models.CharField(max_length=255, blank=True)
    smallUnitBarCode = models.CharField(max_length=255, blank=True)
    
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
    storeGroup = models.CharField(max_length=255, blank=True)  # As per schema, this is a string field
    
    def __str__(self):
        return self.storeName
    
    class Meta:
        ordering = ['storeName']
        db_table = 'stores'
