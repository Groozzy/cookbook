import json
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data/ingredients.json', encoding='utf-8') as data:
            for ingredients in json.loads(data.read()):
                Ingredient.objects.get_or_create(**ingredients)
