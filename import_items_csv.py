import os
import django
import csv

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tantawy.settings')
django.setup()

from django.db import connection
from core.models import Item, ItemsGroup

def truncate_items_table():
    """Truncate the items table and reset the auto-increment ID"""
    print("Truncating items table...")
    
    with connection.cursor() as cursor:
        # Delete all items
        Item.objects.all().delete()
        
        # Reset the PostgreSQL sequence for the items table
        cursor.execute("ALTER SEQUENCE core_item_id_seq RESTART WITH 1;")
    
    print("Items table truncated and IDs reset!")

def import_items_from_csv():
    csv_file = 'items.csv'
    
    # Truncate table first
    truncate_items_table()
    
    # Read the CSV file with Windows-1256 encoding
    with open(csv_file, 'r', encoding='windows-1256') as file:
        csv_reader = csv.reader(file)
        
        items_created = 0
        errors = []
        used_ids = set()
        next_available_id = 1
        
        for row_num, row in enumerate(csv_reader, start=1):
            if len(row) < 3:
                errors.append(f"Row {row_num}: Insufficient data - {row}")
                continue
            
            try:
                original_item_id = int(row[0].strip())
                item_name = row[1].strip()
                item_group_id = int(row[2].strip()) if row[2].strip() else None
                
                # Check if ID is already used
                item_id = original_item_id
                if item_id in used_ids:
                    # Find next available ID
                    while next_available_id in used_ids:
                        next_available_id += 1
                    item_id = next_available_id
                    print(f"Warning: Duplicate ID {original_item_id} detected. Assigning new ID {item_id} to '{item_name}'")
                
                used_ids.add(item_id)
                
                # Try to find the ItemsGroup
                item_group = None
                if item_group_id:
                    try:
                        item_group = ItemsGroup.objects.get(id=item_group_id)
                    except ItemsGroup.DoesNotExist:
                        errors.append(f"Row {row_num}: ItemsGroup with id {item_group_id} not found for item '{item_name}'")
                
                # Create new item with explicit ID
                Item.objects.create(
                    id=item_id,
                    itemGroupId=item_group,
                    itemName=item_name,
                    isUsed=True,
                    isTax=False,
                    mainUnitPack=0,
                    subUnitPack=0
                )
                items_created += 1
                print(f"Created: ID={item_id}, {item_name} (Group ID: {item_group_id})")
                    
            except ValueError as e:
                errors.append(f"Row {row_num}: Invalid data format - {row} - {str(e)}")
            except Exception as e:
                errors.append(f"Row {row_num}: Error - {str(e)}")
        
        # Print summary
        print("\n" + "="*50)
        print("IMPORT SUMMARY")
        print("="*50)
        print(f"Items created: {items_created}")
        print(f"Errors: {len(errors)}")
        
        if errors:
            print("\nERRORS:")
            for error in errors:
                print(f"  - {error}")

if __name__ == '__main__':
    print("Starting CSV import...")
    import_items_from_csv()
    print("\nImport completed!")
