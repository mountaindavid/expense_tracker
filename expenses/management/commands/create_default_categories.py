from django.core.management.base import BaseCommand
from expenses.models import Category

class Command(BaseCommand):
    help = 'Creates default parent categories'

    def handle(self, *args, **options):
        categories = [
            'Transport', 'Food & Dining', 'Housing', 'Entertainment', 
            'Health & Fitness', 'Shopping', 'Education', 'Travel', 
            'Insurance', 'Investments', 'Subscriptions', 'Gifts & Donations', 
            'Business', 'Pets', 'Miscellaneous'
        ]

        created_count = 0
        for name in categories:
            category, created = Category.objects.get_or_create(
                name=name, 
                defaults={'is_custom': False}
            )
            if created:
                self.stdout.write(f"Created: {name}")
                created_count += 1
            else:
                self.stdout.write(f"Already exists: {name}")

        self.stdout.write(f'Successfully created {created_count} categories')