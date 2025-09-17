# Custom migration to fix ALL audit fields (createdAt, createdBy, updatedAt, updatedBy, deletedAt, deletedBy) for all models
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_fix_updatedAt_nullable'),
    ]

    operations = [
        # Fix ALL audit fields for ALL models
        
        # Account model
        migrations.AlterField(
            model_name='account',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created'),
        ),
        migrations.AlterField(
            model_name='account',
            name='createdBy',
            field=models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='account',
            name='deletedAt',
            field=models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='deletedBy',
            field=models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='account',
            name='updatedBy',
            field=models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL),
        ),

        # Transaction model
        migrations.AlterField(
            model_name='transaction',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='createdBy',
            field=models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='deletedAt',
            field=models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='deletedBy',
            field=models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True, blank=True, help_text='Timestamp when record was last updated', null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='updatedBy',
            field=models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL),
        ),

        # ItemsGroup model
        migrations.AlterField(
            model_name='itemsgroup',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created'),
        ),
        migrations.AlterField(
            model_name='itemsgroup',
            name='createdBy',
            field=models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='itemsgroup',
            name='deletedAt',
            field=models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True),
        ),
        migrations.AlterField(
            model_name='itemsgroup',
            name='deletedBy',
            field=models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='itemsgroup',
            name='updatedBy',
            field=models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL),
        ),

        # Item model
        migrations.AlterField(
            model_name='item',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created'),
        ),
        migrations.AlterField(
            model_name='item',
            name='createdBy',
            field=models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='deletedAt',
            field=models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='deletedBy',
            field=models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='updatedBy',
            field=models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL),
        ),

        # PriceList model
        migrations.AlterField(
            model_name='pricelist',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created'),
        ),
        migrations.AlterField(
            model_name='pricelist',
            name='createdBy',
            field=models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pricelist',
            name='deletedAt',
            field=models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True),
        ),
        migrations.AlterField(
            model_name='pricelist',
            name='deletedBy',
            field=models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pricelist',
            name='updatedBy',
            field=models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL),
        ),

        # PriceListDetail model
        migrations.AlterField(
            model_name='pricelistdetail',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created'),
        ),
        migrations.AlterField(
            model_name='pricelistdetail',
            name='createdBy',
            field=models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pricelistdetail',
            name='deletedAt',
            field=models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True),
        ),
        migrations.AlterField(
            model_name='pricelistdetail',
            name='deletedBy',
            field=models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pricelistdetail',
            name='updatedBy',
            field=models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL),
        ),

        # StoreGroup model
        migrations.AlterField(
            model_name='storegroup',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created'),
        ),
        migrations.AlterField(
            model_name='storegroup',
            name='createdBy',
            field=models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='storegroup',
            name='deletedAt',
            field=models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True),
        ),
        migrations.AlterField(
            model_name='storegroup',
            name='deletedBy',
            field=models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='storegroup',
            name='updatedBy',
            field=models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL),
        ),

        # Store model
        migrations.AlterField(
            model_name='store',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created'),
        ),
        migrations.AlterField(
            model_name='store',
            name='createdBy',
            field=models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='store',
            name='deletedAt',
            field=models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='deletedBy',
            field=models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='store',
            name='updatedBy',
            field=models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL),
        ),

        # CustomerVendor model
        migrations.AlterField(
            model_name='customervendor',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created'),
        ),
        migrations.AlterField(
            model_name='customervendor',
            name='createdBy',
            field=models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customervendor',
            name='deletedAt',
            field=models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True),
        ),
        migrations.AlterField(
            model_name='customervendor',
            name='deletedBy',
            field=models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customervendor',
            name='updatedBy',
            field=models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL),
        ),

        # InvoiceMaster model
        migrations.AlterField(
            model_name='invoicemaster',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created'),
        ),
        migrations.AlterField(
            model_name='invoicemaster',
            name='createdBy',
            field=models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoicemaster',
            name='deletedAt',
            field=models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True),
        ),
        migrations.AlterField(
            model_name='invoicemaster',
            name='deletedBy',
            field=models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoicemaster',
            name='updatedBy',
            field=models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL),
        ),

        # InvoiceDetail model
        migrations.AlterField(
            model_name='invoicedetail',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created'),
        ),
        migrations.AlterField(
            model_name='invoicedetail',
            name='createdBy',
            field=models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoicedetail',
            name='deletedAt',
            field=models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True),
        ),
        migrations.AlterField(
            model_name='invoicedetail',
            name='deletedBy',
            field=models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoicedetail',
            name='updatedBy',
            field=models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]