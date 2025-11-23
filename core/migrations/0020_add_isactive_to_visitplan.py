# Generated manually to add isActive field to VisitPlan

from django.db import migrations, models


def add_isactive_field(apps, schema_editor):
    """Add isActive column using raw SQL"""
    schema_editor.execute(
        'ALTER TABLE "visitPlans" ADD COLUMN IF NOT EXISTS "isActive" BOOLEAN DEFAULT FALSE NOT NULL;'
    )


def remove_isactive_field(apps, schema_editor):
    """Remove isActive column using raw SQL"""
    schema_editor.execute(
        'ALTER TABLE "visitPlans" DROP COLUMN IF EXISTS "isActive";'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_add_visitplan_model'),
    ]

    operations = [
        migrations.RunPython(add_isactive_field, remove_isactive_field),
    ]
