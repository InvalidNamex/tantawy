# Custom migration to fix NULL handling for optional fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_accounting_models'),
    ]

    operations = [
        # Update Item model fields to allow NULL
        migrations.AlterField(
            model_name='item',
            name='itemImage',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='barcode',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='sign',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='mainUnitName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='subUnitName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='smallUnitName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='subUnitBarCode',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='smallUnitBarCode',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        
        # Update Store model field to allow NULL
        migrations.AlterField(
            model_name='store',
            name='storeGroup',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        
        # Update CustomerVendor model fields to allow NULL
        migrations.AlterField(
            model_name='customervendor',
            name='phone_one',
            field=models.CharField(blank=True, help_text='Primary phone number', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customervendor',
            name='phone_two',
            field=models.CharField(blank=True, help_text='Secondary phone number', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customervendor',
            name='notes',
            field=models.TextField(blank=True, help_text='Additional notes or comments', null=True),
        ),
        
        # Update InvoiceMaster model fields to allow NULL
        migrations.AlterField(
            model_name='invoicemaster',
            name='notes',
            field=models.TextField(blank=True, help_text='Invoice notes or comments', null=True),
        ),
        
        # Update InvoiceDetail model fields to allow NULL
        migrations.AlterField(
            model_name='invoicedetail',
            name='notes',
            field=models.TextField(blank=True, help_text='Line item notes', null=True),
        ),
        
        # Update Transaction model fields to allow NULL
        migrations.AlterField(
            model_name='transaction',
            name='notes',
            field=models.TextField(blank=True, help_text='Transaction notes', null=True),
        ),
    ]