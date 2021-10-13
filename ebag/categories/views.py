from categories.forms import CategoryManage, SimilarityManage
from categories.models import Category, Similarity
from categories.serializers import CategorySerializer, SimilaritySerializer
from categories.utils import (
    get_category_islands_to_string,
    get_category_nodes,
    get_category_parents,
    get_category_siblings,
    get_category_similarities,
    get_category_tree_to_string,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import viewsets


def index(request):
    root_name = Category.ROOT_NAME
    category_count = Category.objects.exclude(name=root_name).count()
    similarity_count = Similarity.objects.count()

    category_root_tree = ''
    category_root_islands = ''

    if Category.objects.filter(name=root_name).exists():
        root_node = Category.objects.get(name=root_name)
        category_root_tree = get_category_tree_to_string(root_node)
        category_root_islands = get_category_islands_to_string(root_node)

    context = {
        'root_name': root_name,
        'category_count': category_count,
        'similarity_count': similarity_count,
        'category_root_tree': category_root_tree,
        'category_root_islands': category_root_islands,
    }
    return render(request, 'index.html', context=context)


def access_denied(request):
    return render(request, 'categories/access_denied.html')


def category_manage(request, pk=None, slug=None):
    if pk:
        manage_type = 'update'
        category = get_object_or_404(Category, id=pk)
    else:
        manage_type = 'create'
        category = None

    form = CategoryManage(request.POST or None, request.FILES or None, instance=category)

    context = {
        'pk': pk,
        'slug': slug,
        'form': form,
        'manage_type': manage_type,
    }

    if form.is_valid():
        if category and category.name == Category.ROOT_NAME:
            return redirect('categories:access_denied')
        category = form.save()
        return redirect(category)
    return render(request, 'categories/category_manage.html', context)


class CategoryList(generic.ListView):
    queryset = Category.objects.exclude(name=Category.ROOT_NAME)
    context_object_name = 'category_list'


class CategoryDisplay(generic.DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_island'] = get_category_islands_to_string(self.object)
        context['category_nodes'] = get_category_nodes(self.object)
        context['category_parents'] = get_category_parents(self.object)
        context['category_siblings'] = get_category_siblings(self.object)
        context['category_similarities'] = get_category_similarities(self.object)
        context['category_tree'] = get_category_tree_to_string(self.object)
        return context


class CategoryDelete(generic.edit.DeleteView):
    model = Category
    template_name = 'categories/category_delete.html'
    success_url = reverse_lazy('categories:index')

    def post(self, request, *args, **kwargs):
        if self.get_object().name == Category.ROOT_NAME:
            return redirect('categories:access_denied')
        return super().post(request, *args, **kwargs)


def similarity_manage(request, pk=None):
    if pk:
        manage_type = 'update'
        similarity = get_object_or_404(Similarity, id=pk)
    else:
        manage_type = 'create'
        similarity = None

    form = SimilarityManage(request.POST or None, instance=similarity)

    category_count = Category.objects.exclude(name=Category.ROOT_NAME).count()

    context = {
        'pk': pk,
        'form': form,
        'manage_type': manage_type,
        'category_count': category_count,
    }

    if form.is_valid():
        similarity = form.save()
        return redirect(similarity)
    return render(request, 'categories/similarity_manage.html', context)


class SimilarityList(generic.ListView):
    model = Similarity


class SimilarityDisplay(generic.DetailView):
    model = Similarity


class SimilarityDelete(generic.edit.DeleteView):
    model = Similarity
    template_name = 'categories/similarity_delete.html'
    success_url = reverse_lazy('categories:index')


# REST ViewSets

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SimilarityViewSet(viewsets.ModelViewSet):
    queryset = Similarity.objects.all()
    serializer_class = SimilaritySerializer
