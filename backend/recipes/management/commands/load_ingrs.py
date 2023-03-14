import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient

DATA_ROOT = os.path.join(settings.BASE_DIR, "data")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "filename", default="ingredients.csv", nargs="?", type=str
        )

    def handle(self, *args, **options):
        try:
            with open(
                os.path.join(DATA_ROOT, options["filename"]),
                "r",
                encoding="utf-8",
            ) as file:
                data = csv.reader(file)
                for name, measurement_unit in data:
                    Ingredient.objects.get_or_create(
                        name=name, measurement_unit=measurement_unit
                    )
        except FileNotFoundError:
            raise CommandError(
                "Добавьте файл 'ingredients' в директорию 'data'"
            )
