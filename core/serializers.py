from rest_framework import serializers
from core.models import *

class ItemsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsGroup
        fields = ['id', 'itemsGroupName', 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 'deletedBy', 'isDeleted']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'itemGroupId', 'itemName', 'itemImage', 'barcode', 'sign', 'isUsed', 'isTax', 
                 'mainUnitName', 'subUnitName', 'smallUnitName', 'mainUnitPack', 'subUnitPack', 
                 'subUnitBarCode', 'smallUnitBarCode', 'createdAt', 'updatedAt', 'deletedAt', 
                 'createdBy', 'updatedBy', 'deletedBy', 'isDeleted']

class PriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceList
        fields = ['id', 'priceListName', 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 'deletedBy', 'isDeleted']

class PriceListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceListDetail
        fields = ['id', 'priceList', 'item', 'price', 'createdAt', 'updatedAt', 'deletedAt', 
                 'createdBy', 'updatedBy', 'deletedBy', 'isDeleted']

class StoreGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreGroup
        fields = ['id', 'storeGroupName', 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 'deletedBy', 'isDeleted']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'storeName', 'storeGroup', 'createdAt', 'updatedAt', 'deletedAt', 'createdBy', 'updatedBy', 'deletedBy', 'isDeleted']
