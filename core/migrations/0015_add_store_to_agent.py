# Generated manually to add storeID field to Agent model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_rename_agentid_column'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='storeID',
            field=models.ForeignKey(blank=True, help_text='Store assigned to this agent', null=True, on_delete=django.db.models.deletion.PROTECT, to='core.store', db_column='storeID'),
        ),
    ]