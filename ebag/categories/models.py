import re

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def set_parent():
    try:
        return Category.objects.get(name=Category.ROOT_NAME)
    except Category.DoesNotExist:
        return None


class Category(models.Model):
    """
    Define (Sub)Categories
    """
    ROOT_NAME = 'root'

    name = models.CharField(
        max_length=200,
        help_text='Enter a unique name.',
    )
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='categories/')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET(set_parent),
        related_name='sub_categories',
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories:category_display', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        self.name = re.sub(r'\s+', ' ', self.name).strip()
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Similarity(models.Model):
    """
    Define Category Similarities
    """
    node_one = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='related_node_one',
    )
    node_two = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='related_node_two',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.node_one.name} - {self.node_two.name}'

    def get_absolute_url(self):
        return reverse('categories:similarity_display', args=[self.id])
