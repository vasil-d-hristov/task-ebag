import re

from categories.models import Category, Similarity
from categories.utils import get_category_tree_nodes
from django import forms
from django.utils.text import slugify


class CategoryManage(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'parent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category = kwargs.get('instance')
        if category:
            category_tree_nodes = get_category_tree_nodes(category)
            category_queryset = Category.objects.exclude(id__in=category_tree_nodes)
            self.fields['parent'].queryset = category_queryset

    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data.get('name')
        name = re.sub(r'\s+', ' ', name).strip()
        if not re.search(r'^[ _a-zA-Z0-9-]+$', name):
            raise forms.ValidationError('The Name must be Alphanumeric.')

        slug = slugify(name)
        if Category.objects.filter(slug=slug).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Category with this Name already exists.')


class SimilarityManage(forms.ModelForm):
    class Meta:
        model = Similarity
        fields = ['node_one', 'node_two']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        similarity_queryset = Category.objects.exclude(name=Category.ROOT_NAME)
        self.fields['node_one'].queryset = similarity_queryset
        self.fields['node_two'].queryset = similarity_queryset

    def clean(self):
        cleaned_data = super().clean()

        node_one = cleaned_data.get('node_one')
        node_two = cleaned_data.get('node_two')
        if node_one and node_two:
            if node_one == node_two:
                raise forms.ValidationError('First and second Nodes cannot be the same.')
            if Similarity.objects.filter(node_one=node_one, node_two=node_two).exclude(id=self.instance.id).exists():
                raise forms.ValidationError('Such similar Similarity already exists.')
            if Similarity.objects.filter(node_one=node_two, node_two=node_one).exclude(id=self.instance.id).exists():
                raise forms.ValidationError('Such mirror Similarity already exists.')
