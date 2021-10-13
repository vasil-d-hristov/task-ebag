import os

from categories.models import Category, Similarity
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


def create_category(name, parent=None):
    if parent:
        file_name = 'cat01.jpg'
    else:
        file_name = 'castle.jpg'

    file_path = os.path.join(settings.BASE_DIR, 'categories', 'tests', 'files', file_name)

    with open(file_path, 'rb') as file_upload:
        image = SimpleUploadedFile(file_upload.name, file_upload.read())

    description = (
        'A category description is a paragraph or two of content on '
        'the page representing an entire category of items for sale.'
    )

    return Category.objects.create(name=name, description=description, image=image, parent=parent)


def create_similarity(node_one, node_two):
    return Similarity.objects.create(node_one=node_one, node_two=node_two)
