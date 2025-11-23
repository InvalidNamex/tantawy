# Generated manually to fix agentbalanceview

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_add_isactive_to_visitplan'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
            DROP VIEW IF EXISTS agentbalanceview;
            
            CREATE VIEW agentbalanceview AS
            SELECT 
                a.id AS agentid,
                a."agentName" AS agentname,
                a."agentUsername" AS agentusername,
                COALESCE(SUM(t.debit), 0) AS totaldebit,
                COALESCE(SUM(t.credit), 0) AS totalcredit,
                COALESCE(SUM(t.credit), 0) - COALESCE(SUM(t.debit), 0) AS balance
            FROM agents a
            LEFT JOIN transactions t ON a.id = t."agentID" AND t."isDeleted" = FALSE
            WHERE a."isDeleted" = FALSE
            GROUP BY a.id, a."agentName", a."agentUsername"
            ORDER BY a.id;
            ''',
            reverse_sql='DROP VIEW IF EXISTS agentbalanceview;'
        ),
    ]
