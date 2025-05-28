from django.urls import path
from . import views

app_name='main'

urlpatterns = [
    path('',views.index,name='index'),
    path('calculator/',views.calculator,name='calculator'),
    path('privacy_policy/',views.privacy_policy,name='privacy_policy'),
    path('product_list/',views.product_list,name='product_list'),
    path('product/<slug:slug>/',views.product,name='product'),
    path('reels/',views.reels,name='reels'),
    path('seller/',views.seller,name='seller'),
    path('terms_and_conditions/',views.terms_and_conditions,name='terms_and_conditions'),
    path('get_child_categories/<int:parent_id>/', views.get_child_categories, name='get_child_categories'),

]
