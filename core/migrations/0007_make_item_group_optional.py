# Generated manually to make itemGroupId optional

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_fix_all_audit_fields_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='itemGroupId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.itemsgroup'),
        ),
    ]