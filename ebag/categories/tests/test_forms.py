import os

from categories.forms import CategoryManage, SimilarityManage
from categories.models import Category
from categories.tests.utils import create_category, create_similarity
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class CategoryManageFormTests(TestCase):

    def setUp(self):
        self.root_node = create_category(Category.ROOT_NAME)
        self.test_node = create_category('T1', self.root_node)

    def test_form_category_manage_is_valid(self):
        data = {
            'name': 'T2',
            'description': 'test',
            'parent': self.root_node,
        }
        file_path = os.path.join(settings.BASE_DIR, r'categories\tests\files\cat01.jpg')
        with open(file_path, 'rb') as file_upload:
            data_file = {'image': SimpleUploadedFile(file_upload.name, file_upload.read())}
        form = CategoryManage(data, data_file)
        self.assertTrue(form.is_valid())

    def test_form_category_manage_is_not_valid_due_to_name_duplication(self):
        data = {
            'name': 'T1',
            'description': 'test',
            'parent': self.root_node,
        }
        file_path = os.path.join(settings.BASE_DIR, r'categories\tests\files\cat01.jpg')
        with open(file_path, 'rb') as file_upload:
            data_file = {'image': SimpleUploadedFile(file_upload.name, file_upload.read())}
        form = CategoryManage(data, data_file)
        self.assertFalse(form.is_valid())


class SimilarityManageFormTests(TestCase):

    def setUp(self):
        self.root_node = create_category(Category.ROOT_NAME)
        self.test_node_1 = create_category('T1', self.root_node)
        self.test_node_2 = create_category('T2', self.root_node)
        self.test_node_3 = create_category('T3', self.root_node)
        self.test_similarity = create_similarity(self.test_node_1, self.test_node_2)

    def test_form_similarity_manage_is_valid(self):
        data = {
            'node_one': self.test_node_1,
            'node_two': self.test_node_3,
        }
        form = SimilarityManage(data)
        self.assertTrue(form.is_valid())

    def test_form_similarity_manage_is_not_valid_due_to_similarity_duplication(self):
        data = {
            'node_one': self.test_node_2,
            'node_two': self.test_node_1,
        }
        form = SimilarityManage(data)
        self.assertFalse(form.is_valid())
