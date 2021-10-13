import random

from categories.models import Category, Similarity
from categories.tests.utils import create_category, create_similarity
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create random [c] Categories and [s] Similarities.'

    def add_arguments(self, parser):
        parser.add_argument('-c', '--categories', type=int)
        parser.add_argument('-s', '--similarities', type=int)

    def handle(self, *args, **kwargs):
        count_categories = kwargs.get('categories')
        count_similarities = kwargs.get('similarities')

        Category.objects.all().delete()

        root_node = create_category(Category.ROOT_NAME)

        self.stdout.write(f'Added {str("Root").rjust(16)} {str(1).rjust(8)}')

        categories = []
        similarities = 0

        if count_categories and count_categories > 0:
            for i in range(1, count_categories + 1):
                parent = random.choice(categories + [root_node])
                categories.append(create_category(f'T {i}', parent))
                self.stdout.write(f'Added {str("Category").rjust(16)} {str(i).rjust(8)}')

            if count_similarities and count_similarities > 0:
                for i in range(1, count_similarities + 1):
                    node_one = random.choice(categories)
                    node_two = random.choice(categories)
                    if node_one != node_two:
                        if not Similarity.objects.filter(node_one=node_one, node_two=node_two).exists():
                            if not Similarity.objects.filter(node_one=node_two, node_two=node_one).exists():
                                similarities += 1
                                create_similarity(node_one, node_two)
                                self.stdout.write(f'Added {str("Similarity").rjust(16)} {str(similarities).rjust(8)}')
