import os

from categories.models import Category, Similarity
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


def create_category(name, parent=None):
    if parent:
        file_path = r'categories\tests\files\cat01.jpg'
    else:
        file_path = r'categories\tests\files\castle.jpg'
    file_path = os.path.join(settings.BASE_DIR, file_path)
    with open(file_path, 'rb') as file_upload:
        image = SimpleUploadedFile(file_upload.name, file_upload.read())
        return Category.objects.create(name=name, description='test', image=image, parent=parent)


def create_similarity(node_one, node_two):
    return Similarity.objects.create(node_one=node_one, node_two=node_two)
