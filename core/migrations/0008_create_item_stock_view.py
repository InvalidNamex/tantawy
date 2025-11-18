# Generated manually to create itemStock view

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_make_item_group_optional'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
            CREATE OR REPLACE VIEW "itemStock" AS
            SELECT 
                i.id AS id, 
                i."itemName" AS "itemName",
                i."isDeleted" AS "isDeleted",
                COALESCE(im."storeID_id", id."storeID_id") AS "storeID",
                COALESCE(SUM(
                    CASE 
                        WHEN im."invoiceType" IN (1, 4) AND im."isDeleted" = FALSE THEN id.quantity 
                        ELSE 0 
                    END
                ), 0) 
                - 
                COALESCE(SUM(
                    CASE 
                        WHEN im."invoiceType" IN (2, 3) AND im."isDeleted" = FALSE THEN id.quantity 
                        ELSE 0 
                    END
                ), 0) AS stock
            FROM items i
            LEFT JOIN "invoiceDetail" id ON i.id = id.item_id
            LEFT JOIN "invoiceMaster" im ON id."invoiceMasterID_id" = im.id
            GROUP BY i.id, i."itemName", i."isDeleted", COALESCE(im."storeID_id", id."storeID_id");
            ''',
            reverse_sql='DROP VIEW IF EXISTS "itemStock";'
        ),
    ]