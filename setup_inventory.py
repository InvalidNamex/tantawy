# Setup script for Inventory Management System
# Run this after migrating the database

from django.contrib.auth.models import User, Group

# Create StoreAdmins group if it doesn't exist
store_admins_group, created = Group.objects.get_or_create(name='StoreAdmins')

if created:
    print("✓ Created StoreAdmins group")
else:
    print("✓ StoreAdmins group already exists")

# Get all superusers
superusers = User.objects.filter(is_superuser=True)
print(f"\n✓ Found {superusers.count()} superuser(s)")

# You can manually add users to the StoreAdmins group like this:
# Example:
# user = User.objects.get(username='yourusername')
# user.groups.add(store_admins_group)
# print(f"✓ Added {user.username} to StoreAdmins group")

print("\n" + "="*50)
print("Inventory Management System Setup Complete!")
print("="*50)
print("\nTo add users to StoreAdmins group, use Django admin or:")
print("python manage.py shell < setup_inventory.py")
print("\nOr manually in Django shell:")
print(">>> from django.contrib.auth.models import User, Group")
print(">>> user = User.objects.get(username='your_username')")
print(">>> group = Group.objects.get(name='StoreAdmins')")
print(">>> user.groups.add(group)")
