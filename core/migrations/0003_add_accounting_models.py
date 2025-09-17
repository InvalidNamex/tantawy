# Generated manually for new accounting models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_invoice_models'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created')),
                ('updatedAt', models.DateTimeField(auto_now=True, help_text='Timestamp when record was last updated')),
                ('deletedAt', models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True)),
                ('isDeleted', models.BooleanField(default=False, help_text='Indicates if record is soft deleted')),
                ('accountName', models.TextField(help_text='Name of the account')),
                ('accountGroup', models.BigIntegerField(blank=True, help_text='Account group ID (references cost center)', null=True)),
                ('sign', models.BigIntegerField(blank=True, help_text='Unique sign/code for the account', null=True, unique=True)),
                ('createdBy', models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('deletedBy', models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL)),
                ('updatedBy', models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
                'db_table': 'accounts',
                'ordering': ['accountName'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created')),
                ('updatedAt', models.DateTimeField(auto_now=True, help_text='Timestamp when record was last updated')),
                ('deletedAt', models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True)),
                ('isDeleted', models.BooleanField(default=False, help_text='Indicates if record is soft deleted')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, help_text='Transaction amount', max_digits=15, null=True)),
                ('notes', models.TextField(blank=True, help_text='Transaction notes')),
                ('type', models.SmallIntegerField(blank=True, choices=[(1, 'Purchase'), (2, 'Sales'), (3, 'Return Purchase'), (4, 'Return Sales')], help_text='Transaction type: 1=Purchase, 2=Sales, 3=Return Purchase, 4=Return Sales', null=True)),
                ('accountID', models.ForeignKey(help_text='Associated account', on_delete=django.db.models.deletion.PROTECT, to='core.account')),
                ('createdBy', models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('customerVendorID', models.ForeignKey(blank=True, help_text='Associated customer or vendor', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.customervendor')),
                ('deletedBy', models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_deleted', to=settings.AUTH_USER_MODEL)),
                ('invoiceID', models.ForeignKey(blank=True, help_text='Associated invoice', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.invoicemaster')),
                ('updatedBy', models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'db_table': 'transactions',
                'ordering': ['-createdAt'],
            },
        ),
    ]