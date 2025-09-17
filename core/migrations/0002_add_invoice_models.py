# Generated manually to add invoice models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerVendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('deletedAt', models.DateTimeField(blank=True, null=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('customerVendorName', models.TextField()),
                ('phone_one', models.CharField(blank=True, max_length=255)),
                ('phone_two', models.CharField(blank=True, max_length=255)),
                ('type', models.SmallIntegerField(choices=[(1, 'Customer'), (2, 'Vendor'), (3, 'Both')], default=1)),
                ('notes', models.TextField(blank=True)),
                ('createdBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('deletedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL)),
                ('updatedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'customerVendor',
                'ordering': ['customerVendorName'],
            },
        ),
        migrations.CreateModel(
            name='InvoiceMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('deletedAt', models.DateTimeField(blank=True, null=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('invoiceType', models.IntegerField(choices=[(1, 'Purchases'), (2, 'Sales'), (3, 'Return Purchases'), (4, 'Return Sales')])),
                ('notes', models.TextField(blank=True)),
                ('discountAmount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('discountPercentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('taxAmount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('taxPercentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('netTotal', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('paymentType', models.SmallIntegerField(choices=[(1, 'Cash'), (2, 'Visa'), (3, 'Partial or Deferred')], default=1)),
                ('status', models.SmallIntegerField(choices=[(0, 'Paid'), (1, 'Unpaid'), (2, 'Partially Paid')], default=0)),
                ('totalPaid', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('returnStatus', models.SmallIntegerField(choices=[(0, 'Not Returned'), (1, 'Partially Returned'), (2, 'Fully Returned')], default=0)),
                ('createdBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('customerOrVendorID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.customervendor')),
                ('deletedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL)),
                ('originalInvoiceID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.invoicemaster')),
                ('storeID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.store')),
                ('updatedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'invoiceMaster',
                'ordering': ['-createdAt'],
            },
        ),
        migrations.CreateModel(
            name='InvoiceDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('deletedAt', models.DateTimeField(blank=True, null=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('quantity', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('notes', models.TextField(blank=True)),
                ('discountAmount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('discountPercentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('taxAmount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('taxPercentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('createdBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('deletedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL)),
                ('invoiceMasterID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.invoicemaster')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.item')),
                ('storeID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.store')),
                ('updatedBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'invoiceDetail',
                'ordering': ['invoiceMasterID', 'item'],
            },
        ),
    ]