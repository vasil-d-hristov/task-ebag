from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.index, name='index'),
    path('access-denied', views.access_denied, name='access_denied'),
    path('category-list/', views.CategoryList.as_view(), name='category_list'),
    path('category-create/', views.category_manage, name='category_create'),
    path('category/<int:pk>/<slug:slug>/', views.CategoryDisplay.as_view(), name='category_display'),
    path('category/<int:pk>/<slug:slug>/update/', views.category_manage, name='category_update'),
    path('category/<int:pk>/<slug:slug>/delete/', views.CategoryDelete.as_view(), name='category_delete'),
    path('similarity-list/', views.SimilarityList.as_view(), name='similarity_list'),
    path('similarity-create/', views.similarity_manage, name='similarity_create'),
    path('similarity/<int:pk>/', views.SimilarityDisplay.as_view(), name='similarity_display'),
    path('similarity/<int:pk>/update/', views.similarity_manage, name='similarity_update'),
    path('similarity/<int:pk>/delete/', views.SimilarityDelete.as_view(), name='similarity_delete'),
]
