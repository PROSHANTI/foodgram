import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from api.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'loading ingredients from data in json'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='ingredients.json', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        with open(
                os.path.join(
                    DATA_ROOT,
                    options['filename']), 'r', encoding='utf-8') as f:
            data = json.load(f)
            for ingredient in data:
                obj, created = Ingredient.objects.get_or_create(
                    name=ingredient["name"],
                    defaults={
                        'measurement_unit': ingredient["measurement_unit"]
                    }
                )
                if not created:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Ингредиент {ingredient["name"]} '
                            f'{ingredient["measurement_unit"]} '
                            f'уже есть в базе'))
