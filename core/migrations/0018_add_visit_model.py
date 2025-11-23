# Generated manually for Visit model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_placeholder_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created')),
                ('updatedAt', models.DateTimeField(auto_now=True, blank=True, help_text='Timestamp when record was last updated', null=True)),
                ('deletedAt', models.DateTimeField(blank=True, help_text='Timestamp when record was soft deleted', null=True)),
                ('isDeleted', models.BooleanField(default=False, help_text='Indicates if record is soft deleted')),
                ('transType', models.SmallIntegerField(choices=[(1, 'Sales'), (2, 'Return Sales'), (3, 'Receive Voucher'), (4, 'Pay Voucher')], help_text='Type of visit: 1=Sales, 2=Return Sales, 3=Receive Voucher, 4=Pay Voucher')),
                ('date', models.DateTimeField(help_text='Date and time of the visit')),
                ('latitude', models.DecimalField(decimal_places=7, help_text='Latitude coordinate of visit location', max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=7, help_text='Longitude coordinate of visit location', max_digits=10)),
                ('notes', models.TextField(blank=True, help_text='Additional notes about the visit', null=True)),
                ('agentID', models.ForeignKey(db_column='agentID', help_text='Agent who made the visit', on_delete=django.db.models.deletion.PROTECT, to='core.agent')),
                ('createdBy', models.ForeignKey(blank=True, help_text='User who created this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='visit_created', to='auth.user')),
                ('customerVendor', models.ForeignKey(blank=True, help_text='Associated customer or vendor (nullable for pay vouchers)', null=True, on_delete=django.db.models.deletion.PROTECT, to='core.customervendor')),
                ('deletedBy', models.ForeignKey(blank=True, help_text='User who soft deleted this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='visit_deleted', to='auth.user')),
                ('updatedBy', models.ForeignKey(blank=True, help_text='User who last updated this record', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='visit_updated', to='auth.user')),
            ],
            options={
                'verbose_name': 'Visit',
                'verbose_name_plural': 'Visits',
                'db_table': 'visits',
                'ordering': ['-date'],
            },
            bases=(models.Model,),
        ),
    ]