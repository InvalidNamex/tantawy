"""
Management command to set default price list for all customer/vendor records
"""
from django.core.management.base import BaseCommand
from core.models import CustomerVendor, PriceList, CustomerVendorPriceList
from django.db import transaction


class Command(BaseCommand):
    help = 'Set default price list (ID=2) for all customer/vendor records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pricelist-id',
            type=int,
            default=2,
            help='Price list ID to set as default (default: 2)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes'
        )

    def handle(self, *args, **options):
        pricelist_id = options['pricelist_id']
        dry_run = options['dry_run']

        # Verify price list exists
        try:
            pricelist = PriceList.objects.get(id=pricelist_id, isDeleted=False)
            self.stdout.write(f"Target Price List: {pricelist.priceListName} (ID: {pricelist_id})")
        except PriceList.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Price list with ID {pricelist_id} does not exist or is deleted')
            )
            return

        # Get all customer/vendor records without a price list mapping
        all_customers = CustomerVendor.objects.filter(isDeleted=False)
        customers_with_mapping = CustomerVendorPriceList.objects.filter(
            isDeleted=False
        ).values_list('customerVendorID', flat=True)
        
        customers_without_pricelist = all_customers.exclude(id__in=customers_with_mapping)

        # Get customers with different price list
        customers_with_different_pricelist_ids = CustomerVendorPriceList.objects.filter(
            isDeleted=False
        ).exclude(priceListID_id=pricelist_id).values_list('customerVendorID', flat=True)
        
        customers_with_different_pricelist = all_customers.filter(id__in=customers_with_different_pricelist_ids)

        total_count = all_customers.count()
        without_pricelist_count = customers_without_pricelist.count()
        with_different_pricelist_count = customers_with_different_pricelist.count()
        already_correct_count = total_count - without_pricelist_count - with_different_pricelist_count

        self.stdout.write("\n" + "="*70)
        self.stdout.write(f"Total active customers/vendors: {total_count}")
        self.stdout.write(f"  - Without price list: {without_pricelist_count}")
        self.stdout.write(f"  - With different price list: {with_different_pricelist_count}")
        self.stdout.write(f"  - Already set to price list {pricelist_id}: {already_correct_count}")
        self.stdout.write("="*70 + "\n")

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made\n'))
            
            if without_pricelist_count > 0:
                self.stdout.write(f"\nWould set price list for {without_pricelist_count} customers without price list:")
                for customer in customers_without_pricelist[:5]:
                    self.stdout.write(f"  - ID {customer.id}: {customer.customerVendorName} (currently: None)")
                if without_pricelist_count > 5:
                    self.stdout.write(f"  ... and {without_pricelist_count - 5} more")

            if with_different_pricelist_count > 0:
                self.stdout.write(f"\nWould update price list for {with_different_pricelist_count} customers with different price list:")
                for customer in customers_with_different_pricelist[:5]:
                    # Get current price list for this customer
                    current_mapping = CustomerVendorPriceList.objects.filter(
                        customerVendorID=customer,
                        isDeleted=False
                    ).first()
                    current_name = current_mapping.priceListID.priceListName if current_mapping else 'None'
                    self.stdout.write(f"  - ID {customer.id}: {customer.customerVendorName} (currently: {current_name})")
                if with_different_pricelist_count > 5:
                    self.stdout.write(f"  ... and {with_different_pricelist_count - 5} more")

            self.stdout.write(self.style.WARNING(f'\nTo apply changes, run without --dry-run flag'))
            return

        # Apply updates
        with transaction.atomic():
            # First, update existing mappings to the target price list
            updated_existing = CustomerVendorPriceList.objects.filter(
                isDeleted=False
            ).update(priceListID_id=pricelist_id)
            
            # Then, create new mappings for customers without any mapping
            new_mappings = []
            for customer in customers_without_pricelist:
                new_mappings.append(
                    CustomerVendorPriceList(
                        customerVendorID=customer,
                        priceListID_id=pricelist_id
                    )
                )
            
            created_count = len(CustomerVendorPriceList.objects.bulk_create(new_mappings))
            
            total_updated = updated_existing + created_count

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully processed {total_updated} customer/vendor records')
        )
        self.stdout.write(
            self.style.SUCCESS(f'  - Updated {updated_existing} existing mappings')
        )
        self.stdout.write(
            self.style.SUCCESS(f'  - Created {created_count} new mappings')
        )
        self.stdout.write(
            self.style.SUCCESS(f'\nAll active customers now have price list: {pricelist.priceListName} (ID: {pricelist_id})')
        )
