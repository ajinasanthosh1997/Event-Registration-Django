# urls.py

from django.urls import path
from .views import IndexView, ProductListView, ProductDetailView

app_name= 'jeweller'

urlpatterns = [
    path('<slug:slug>/', IndexView.as_view(), name='index'),  # Home page
    path('products/', ProductListView.as_view(), name='product_list'),  # Product list page
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),  # Product details page
]
