from django.core.management.base import BaseCommand
from app.models import Product

class Command(BaseCommand):
    help = 'Update features for all products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Updating product features...')
        products = Product.objects.all()
        for product in products:
            product.extract_features()
            product.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated product features'))