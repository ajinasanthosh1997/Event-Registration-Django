from django.urls import path
from . import views
from .views import *


app_name='dashboard'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('home/',DashboardView.as_view(), name='home'),
    path('productlist/',ProductListView.as_view(), name='productlist'),
    path('products/add/', views.product_form_view, name='add_product'),
    path('products/edit/<slug:slug>/', views.product_form_view, name='edit_product'),
    # path('update-product/', views.update_product, name='update_product'),
    path('delete_product/<slug:slug>/', views.delete_product, name='delete_product'),

    path('categorylist/', CategoryListView.as_view(), name='category_list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/edit/<slug:slug>/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/delete/<slug:slug>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('user_login/', views.user_login, name='user_login'),

    path('testimonials/', TestimonialListView.as_view(), name='testimonial_list'),
    path('testimonials/add/', TestimonialCreateView.as_view(), name='testimonial_add'),
    path('testimonials/edit/<slug:slug>/', TestimonialUpdateView.as_view(), name='testimonial_edit'),
    # path('testimonials/delete/<int:pk>/', TestimonialDeleteView.as_view(), name='testimonial_delete'),

    path('jewellers/', JewellerListView.as_view(), name='jeweller_list'),
    path('jewellers/add/', JewellerCreateView.as_view(), name='jeweller_add'),
    path('jewellers/edit/<slug:slug>/', JewellerUpdateView.as_view(), name='jeweller_edit'),
    path('jewellers/delete/<slug:slug>/', JewellerDeleteView.as_view(), name='jeweller_delete'),

    path('jewellery/', JewelleryListView.as_view(), name='jewellery_list'),
    path('jewellery/add/', JewelleryCreateView.as_view(), name='jewellery_add'),
    path('jewellery/edit/<slug:slug>/', JewelleryUpdateView.as_view(), name='jewellery_edit'),
    # path('jewellery/delete/<int:pk>/', JewelleryDeleteView.as_view(), name='jeweller_delete'),

    path('category/', views.JewellerCategoryListView.as_view(), name='jeweller_category_list'),
    path('category/add/', views.JewellerCategoryCreateView.as_view(), name='jeweller_category_add'),
    path('category/<slug:slug>/edit/', views.JewellerCategoryUpdateView.as_view(), name='jeweller_category_edit'),
    # path('category/<int:pk>/delete/', views.JewellerCategoryDeleteView.as_view(), name='jeweller_category_delete'),

    path('product/', views.JewellerProductListView.as_view(), name='jeweller_product_list'),
    path('product/add/', views.JewellerProductCreateView.as_view(), name='jeweller_product_add'),
    path('product/<slug:slug>/edit/', views.JewellerProductUpdateView.as_view(), name='jeweller_product_edit'),
    # path('category/<int:pk>/delete/', views.JewellerProductDeleteView.as_view(), name='jeweller_product_delete'),

    path('logout/', views.logout_view, name='logout'),   
]
