from django.urls import path
from .views import BlogsView,BlogDetailView

app_name="blogs"

urlpatterns = [
  
    path('blogs/', BlogsView.as_view(), name='blogs'),
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-details'),
    
   
]