# Generated manually to rename agentID_id column to agentID

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_add_agent_field_to_invoice'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE "invoiceMaster" RENAME COLUMN "agentID_id" TO "agentID";',
            reverse_sql='ALTER TABLE "invoiceMaster" RENAME COLUMN "agentID" TO "agentID_id";',
        ),
    ]