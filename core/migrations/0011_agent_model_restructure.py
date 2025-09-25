# Generated manually for Agent model restructure

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_add_agent_model'),
    ]

    operations = [
        # Remove the old Agent table completely
        migrations.DeleteModel(
            name='Agent',
        ),
        # Create the new Agent table with independent authentication
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True, help_text='Timestamp when record was created')),
                ('updatedAt', models.DateTimeField(auto_now=True, help_text='Timestamp when record was last updated')),
                ('deletedAt', models.DateTimeField(blank=True, help_text='Timestamp when record was deleted (soft delete)', null=True)),
                ('isDeleted', models.BooleanField(default=False, help_text='Whether this record is deleted (soft delete)')),
                ('agentName', models.CharField(help_text='Display name for the agent', max_length=255)),
                ('agentUsername', models.CharField(help_text='Unique username for agent login', max_length=150, unique=True)),
                ('agentPassword', models.CharField(help_text='Hashed password for agent authentication', max_length=128)),
                ('agentEmail', models.EmailField(blank=True, help_text='Agent email address', max_length=254, null=True)),
                ('agentPhone', models.CharField(blank=True, help_text='Agent phone number', max_length=20, null=True)),
                ('isActive', models.BooleanField(default=True, help_text='Whether the agent can login')),
                ('createdBy', models.ForeignKey(help_text='User who created this record', on_delete=models.deletion.CASCADE, related_name='agent_created', to='auth.user')),
                ('deletedBy', models.ForeignKey(blank=True, help_text='User who deleted this record', null=True, on_delete=models.deletion.SET_NULL, related_name='agent_deleted', to='auth.user')),
                ('updatedBy', models.ForeignKey(help_text='User who last updated this record', on_delete=models.deletion.CASCADE, related_name='agent_updated', to='auth.user')),
            ],
            options={
                'verbose_name': 'Agent',
                'verbose_name_plural': 'Agents',
                'db_table': 'agents',
                'ordering': ['agentName'],
            },
        ),
    ]