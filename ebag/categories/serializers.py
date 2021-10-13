from categories.models import Category, Similarity
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image', 'parent', 'created_at', 'updated_at']


class SimilaritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Similarity
        fields = ['node_one', 'node_two', 'created_at', 'updated_at']
