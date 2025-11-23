# Generated manually for VisitPlan model
from django.db import migrations


def create_visitplan_table(apps, schema_editor):
    schema_editor.execute("""
        CREATE TABLE "visitPlans" (
            "id" bigserial NOT NULL PRIMARY KEY,
            "createdAt" timestamp with time zone NOT NULL,
            "updatedAt" timestamp with time zone,
            "deletedAt" timestamp with time zone,
            "isDeleted" boolean NOT NULL DEFAULT false,
            "dateFrom" date NOT NULL,
            "dateTo" date NOT NULL,
            "customers" jsonb NOT NULL,
            "notes" text,
            "agentID" bigint NOT NULL,
            "createdBy_id" integer,
            "deletedBy_id" integer,
            "updatedBy_id" integer,
            CONSTRAINT "visitPlans_agentID_fkey" FOREIGN KEY ("agentID") REFERENCES "agents"("id") DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT "visitPlans_createdBy_id_fkey" FOREIGN KEY ("createdBy_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT "visitPlans_deletedBy_id_fkey" FOREIGN KEY ("deletedBy_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
            CONSTRAINT "visitPlans_updatedBy_id_fkey" FOREIGN KEY ("updatedBy_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
        );
        CREATE INDEX "visitPlans_agentID_idx" ON "visitPlans"("agentID");
        CREATE INDEX "visitPlans_createdBy_id_idx" ON "visitPlans"("createdBy_id");
        CREATE INDEX "visitPlans_deletedBy_id_idx" ON "visitPlans"("deletedBy_id");
        CREATE INDEX "visitPlans_updatedBy_id_idx" ON "visitPlans"("updatedBy_id");
    """)


def drop_visitplan_table(apps, schema_editor):
    schema_editor.execute('DROP TABLE IF EXISTS "visitPlans" CASCADE;')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_add_visit_model'),
    ]

    operations = [
        migrations.RunPython(create_visitplan_table, reverse_code=drop_visitplan_table),
    ]
