# Generated to create StoreAdmins user group

from django.db import migrations


def create_store_admins_group(apps, schema_editor):
    """Create StoreAdmins group with appropriate permissions"""
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    
    # Create StoreAdmins group
    store_admins_group, created = Group.objects.get_or_create(name='StoreAdmins')
    
    if created:
        # Add permissions for inventory management
        # Users in this group can view and manage inventory
        permissions_codenames = [
            'view_item',
            'view_store',
            'view_invoicemaster',
            'add_invoicemaster',
            'view_invoicedetail',
            'add_invoicedetail',
            'view_customervendor',
        ]
        
        for codename in permissions_codenames:
            try:
                permission = Permission.objects.get(codename=codename)
                store_admins_group.permissions.add(permission)
            except Permission.DoesNotExist:
                pass


def remove_store_admins_group(apps, schema_editor):
    """Remove StoreAdmins group"""
    Group = apps.get_model('auth', 'Group')
    try:
        store_admins_group = Group.objects.get(name='StoreAdmins')
        store_admins_group.delete()
    except Group.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_fix_agentbalanceview'),
    ]

    operations = [
        migrations.RunPython(create_store_admins_group, remove_store_admins_group),
    ]
