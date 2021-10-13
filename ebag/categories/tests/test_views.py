import os
import random

from categories.models import Category, Similarity
from categories.tests.utils import create_category, create_similarity
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse


class IndexViewTests(TestCase):

    def test_view_home(self):
        response = self.client.get('/')
        self.assertRedirects(response, reverse('categories:index'))

    def test_view_index_without_database(self):
        link = reverse('categories:index')
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category_count'], 0)
        self.assertEqual(response.context['similarity_count'], 0)
        self.assertEqual(response.context['category_root_tree'], '')
        self.assertEqual(response.context['category_root_islands'], '')

    def test_view_index_with_database(self):
        root_node = create_category(Category.ROOT_NAME)
        test_node_1 = create_category('T1', root_node)
        test_node_2 = create_category('T2', root_node)
        create_similarity(test_node_1, test_node_2)

        link = reverse('categories:index')
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category_count'], 2)
        self.assertEqual(response.context['similarity_count'], 1)
        self.assertNotEqual(response.context['category_root_tree'], '')
        self.assertNotEqual(response.context['category_root_islands'], '')


class CategoryListViewTests(TestCase):

    def test_view_category_list_without_database(self):
        link = reverse('categories:category_list')
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories.')
        self.assertQuerysetEqual(response.context['category_list'], [])

    def test_view_category_list_with_database(self):
        root_node = create_category(Category.ROOT_NAME)
        test_node_1 = create_category('T1', root_node)
        test_node_2 = create_category('T2', root_node)

        link = reverse('categories:category_list')
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'There are no categories.')
        self.assertQuerysetEqual(response.context['category_list'], [test_node_1, test_node_2])


class CategoryCreateViewTests(TestCase):

    def test_view_category_create(self):
        root_node = create_category(Category.ROOT_NAME)

        link_create = reverse('categories:category_create')
        response = self.client.get(link_create)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['manage_type'], 'create')

        data = {
            'name': 'T1',
            'description': 'test',
            'parent': root_node.id,
        }
        file_path = os.path.join(settings.BASE_DIR, r'categories\tests\files\cat01.jpg')
        with open(file_path, 'rb') as file_upload:
            data['image'] = SimpleUploadedFile(file_upload.name, file_upload.read())

        response = self.client.post(link_create, data)

        link_display = reverse('categories:category_display', args=[2, 't1'])
        self.assertRedirects(response, link_display)


class CategoryDisplayViewTests(TestCase):

    def setUp(self):
        self.root_node = create_category(Category.ROOT_NAME)
        self.test_node = create_category('T1', self.root_node)

    def test_view_category_display(self):
        link = reverse('categories:category_display', args=[self.test_node.id, self.test_node.slug])
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)


class CategoryUpdateViewTests(TestCase):

    def setUp(self):
        self.root_node = create_category(Category.ROOT_NAME)
        self.test_node_1 = create_category('T1', self.root_node)
        self.test_node_2 = create_category('T2', self.test_node_1)

    def test_view_category_update(self):
        link_update = reverse('categories:category_update', args=[self.test_node_1.id, self.test_node_1.slug])
        response = self.client.get(link_update)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['manage_type'], 'update')

        form = response.context['form']
        self.assertQuerysetEqual(form.fields['parent'].queryset, [self.root_node])

        data = form.initial
        data['name'] = ' T  11 '

        response = self.client.post(link_update, data)
        self.test_node_1.refresh_from_db()

        link_display = reverse('categories:category_display', args=[self.test_node_1.id, self.test_node_1.slug])
        self.assertRedirects(response, link_display)
        self.assertEqual(self.test_node_1.name, 'T 11')


class CategoryDeleteViewTests(TestCase):

    def setUp(self):
        self.root_node = create_category(Category.ROOT_NAME)
        self.test_node = create_category('T1', self.root_node)

    def test_view_category_delete_on_node_deletion(self):
        link = reverse('categories:category_delete', args=[self.test_node.id, self.test_node.slug])
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.client.post(link)
        response = self.client.get(link)
        self.assertEqual(response.status_code, 404)


class SimilarityListViewTests(TestCase):

    def test_view_similarity_list_without_database(self):
        link = reverse('categories:similarity_list')
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no similarities.')
        self.assertQuerysetEqual(response.context['similarity_list'], [])

    def test_view_similarity_list_with_database(self):
        root_node = create_category(Category.ROOT_NAME)
        test_node_1 = create_category('T1', root_node)
        test_node_2 = create_category('T2', root_node)
        test_node_3 = create_category('T3', root_node)
        test_similarity_1 = create_similarity(test_node_1, test_node_2)
        test_similarity_2 = create_similarity(test_node_2, test_node_3)

        link = reverse('categories:similarity_list')
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'There are no similarities.')
        self.assertQuerysetEqual(response.context['similarity_list'], [test_similarity_1, test_similarity_2])


class SimilarityCreateViewTests(TestCase):

    def test_view_similarity_create_without_database(self):
        link = reverse('categories:similarity_create')
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no enough categories.')
        self.assertEqual(response.context['manage_type'], 'create')

    def test_view_similarity_create_with_database(self):
        root_node = create_category(Category.ROOT_NAME)
        test_node_1 = create_category('T1', root_node)
        test_node_2 = create_category('T2', root_node)

        link_create = reverse('categories:similarity_create')
        response = self.client.get(link_create)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'There are no enough categories.')
        self.assertEqual(response.context['manage_type'], 'create')

        data = {
            'node_one': test_node_1.id,
            'node_two': test_node_2.id,
        }

        response = self.client.post(link_create, data)

        link_display = reverse('categories:similarity_display', args=[1])
        self.assertRedirects(response, link_display)


class SimilarityDisplayViewTests(TestCase):

    def setUp(self):
        self.root_node = create_category(Category.ROOT_NAME)
        self.test_node_1 = create_category('T1', self.root_node)
        self.test_node_2 = create_category('T2', self.root_node)
        self.test_similarity = create_similarity(self.test_node_1, self.test_node_2)

    def test_view_similarity_display(self):
        link = reverse('categories:similarity_display', args=[self.test_similarity.id])
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)


class SimilarityUpdateViewTests(TestCase):

    def setUp(self):
        self.root_node = create_category(Category.ROOT_NAME)
        self.test_node_1 = create_category('T1', self.root_node)
        self.test_node_2 = create_category('T2', self.root_node)
        self.test_similarity = create_similarity(self.test_node_1, self.test_node_2)

    def test_view_similarity_update(self):
        link_update = reverse('categories:similarity_update', args=[self.test_similarity.id])
        response = self.client.get(link_update)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['manage_type'], 'update')

        form = response.context['form']
        self.assertQuerysetEqual(form.fields['node_one'].queryset, [self.test_node_1, self.test_node_2])
        self.assertQuerysetEqual(form.fields['node_two'].queryset, [self.test_node_1, self.test_node_2])

        data = {
            'node_one': self.test_node_2.id,
            'node_two': self.test_node_1.id,
        }

        response = self.client.post(link_update, data)
        self.test_similarity.refresh_from_db()

        link_display = reverse('categories:similarity_display', args=[self.test_similarity.id])
        self.assertRedirects(response, link_display)
        self.assertEqual(self.test_similarity.node_one, self.test_node_2)
        self.assertEqual(self.test_similarity.node_two, self.test_node_1)


class SimilarityDeleteViewTests(TestCase):

    def setUp(self):
        self.root_node = create_category(Category.ROOT_NAME)
        self.test_node_1 = create_category('T1', self.root_node)
        self.test_node_2 = create_category('T2', self.root_node)
        self.test_similarity = create_similarity(self.test_node_1, self.test_node_2)

    def test_view_similarity_delete_on_similarity_deletion(self):
        link = reverse('categories:similarity_delete', args=[self.test_similarity.id])
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.client.post(link)
        response = self.client.get(link)
        self.assertEqual(response.status_code, 404)

    def test_view_similarity_delete_on_node_deletion(self):
        link_delete_similarity = reverse('categories:similarity_delete', args=[self.test_similarity.id])
        response = self.client.get(link_delete_similarity)
        self.assertEqual(response.status_code, 200)
        link_delete_category = reverse('categories:category_delete', args=[self.test_node_1.id, self.test_node_1.slug])
        self.client.post(link_delete_category)
        response = self.client.get(link_delete_similarity)
        self.assertEqual(response.status_code, 404)


class RandomDatabaseViewsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        root_node = create_category(Category.ROOT_NAME)

        categories = []
        similarities = []

        for i in range(1, random.randint(10, 100)):
            parent = random.choice(categories + [root_node])
            categories.append(create_category(f'T {i}', parent))

        for i in range(1, random.randint(10, 100)):
            node_one = random.choice(categories)
            node_two = random.choice(categories)
            if node_one != node_two:
                if not Similarity.objects.filter(node_one=node_one, node_two=node_two).exists():
                    if not Similarity.objects.filter(node_one=node_two, node_two=node_one).exists():
                        similarities.append(create_similarity(node_one, node_two))

        cls.categories = categories
        cls.similarities = similarities

    def test_view_index(self):
        link = reverse('categories:index')
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category_count'], len(self.categories))
        self.assertLessEqual(response.context['similarity_count'], len(self.similarities))

    def test_view_category_list(self):
        link = reverse('categories:category_list')
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'There are no categories.')
        self.assertQuerysetEqual(response.context['category_list'], self.categories, ordered=False)

    def test_view_category_create(self):
        link = reverse('categories:category_create')
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['manage_type'], 'create')

    def test_view_category_display(self):
        for category in self.categories:
            link = category.get_absolute_url()
            response = self.client.get(link)
            self.assertEqual(response.status_code, 200)

    def test_view_similarity_list(self):
        link = reverse('categories:similarity_list')
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'There are no enough categories.')
        self.assertQuerysetEqual(response.context['similarity_list'], self.similarities, ordered=False)

    def test_view_similarity_create(self):
        link = reverse('categories:similarity_create')
        response = self.client.get(link)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'There are no enough categories.')
        self.assertEqual(response.context['manage_type'], 'create')

    def test_view_similarity_display(self):
        for similarity in self.similarities:
            link = similarity.get_absolute_url()
            response = self.client.get(link)
            self.assertEqual(response.status_code, 200)
