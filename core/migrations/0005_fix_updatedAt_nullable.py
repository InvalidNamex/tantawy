# Custom migration to fix updatedAt field to allow NULL
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_fix_optional_fields_null'),
    ]

    operations = [
        # Fix updatedAt field for all models to allow NULL
        migrations.AlterField(
            model_name='account',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True, blank=True, help_text='Timestamp when record was last updated', null=True),
        ),
        migrations.AlterField(
            model_name='customervendor',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True, blank=True, help_text='Timestamp when record was last updated', null=True),
        ),
        migrations.AlterField(
            model_name='invoicedetail',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True, blank=True, help_text='Timestamp when record was last updated', null=True),
        ),
        migrations.AlterField(
            model_name='invoicemaster',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True, blank=True, help_text='Timestamp when record was last updated', null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True, blank=True, help_text='Timestamp when record was last updated', null=True),
        ),
        migrations.AlterField(
            model_name='itemsgroup',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True, blank=True, help_text='Timestamp when record was last updated', null=True),
        ),
        migrations.AlterField(
            model_name='pricelist',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True, blank=True, help_text='Timestamp when record was last updated', null=True),
        ),
        migrations.AlterField(
            model_name='pricelistdetail',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True, blank=True, help_text='Timestamp when record was last updated', null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True, blank=True, help_text='Timestamp when record was last updated', null=True),
        ),
        migrations.AlterField(
            model_name='storegroup',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True, blank=True, help_text='Timestamp when record was last updated', null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True, blank=True, help_text='Timestamp when record was last updated', null=True),
        ),
    ]