from categories.models import Category
from categories.tests.utils import create_category, create_similarity
from django.test import TestCase


class CategoryModelTests(TestCase):

    def setUp(self):
        self.root_node = create_category(Category.ROOT_NAME)
        self.test_node = create_category(' T  1 ', self.root_node)

    def test_model_category_attributes_initial(self):
        self.assertEqual(self.test_node.name, 'T 1')
        self.assertEqual(self.test_node.slug, 't-1')
        self.assertEqual(str(self.test_node), self.test_node.name)
        self.assertEqual(self.test_node.get_absolute_url(), '/categories/category/2/t-1/')

    def test_model_category_attributes_changed(self):
        self.test_node.name = ' T  1  1 '
        self.test_node.save()
        self.assertEqual(self.test_node.name, 'T 1 1')
        self.assertEqual(self.test_node.slug, 't-1-1')
        self.assertEqual(str(self.test_node), self.test_node.name)
        self.assertEqual(self.test_node.get_absolute_url(), '/categories/category/2/t-1-1/')


class SimilarityModelTests(TestCase):

    def setUp(self):
        self.root_node = create_category(Category.ROOT_NAME)
        self.test_node_1 = create_category('T1', self.root_node)
        self.test_node_2 = create_category('T2', self.root_node)
        self.test_similarity = create_similarity(self.test_node_1, self.test_node_2)

    def test_model_similarity_attributes_initial(self):
        self.assertEqual(str(self.test_similarity), f'{self.test_node_1} - {self.test_node_2}')
        self.assertEqual(self.test_similarity.get_absolute_url(), '/categories/similarity/1/')

    def test_model_similarity_attributes_changed(self):
        self.test_similarity.node_one = self.test_node_2
        self.test_similarity.node_two = self.test_node_1
        self.test_similarity.save()
        self.assertEqual(str(self.test_similarity), f'{self.test_node_2} - {self.test_node_1}')
        self.assertEqual(self.test_similarity.get_absolute_url(), '/categories/similarity/1/')
