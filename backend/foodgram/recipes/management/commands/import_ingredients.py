import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт данных из csv в модель Ingredient'

    def handle(self, *args, **options):
        params_for_create = []

        file_path = '../../data/ingredients.csv'
        with open(file_path, 'r', encoding='utf-8') as file:
            ingredients = csv.reader(file)
            for ingredient in ingredients:
                params = {
                    'name': ingredient[0],
                    'measurement_unit': ingredient[1],
                }
                params_for_create.append(params)

        Ingredient.objects.bulk_create(
            [Ingredient(**parameters) for parameters in params_for_create]
        )
