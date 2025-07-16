from django.urls import path
from .views import (HomeView,ContactMessageCreateAPIView,AboutView,
                    GalleryView,ContactView)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),

  
    path('gallery/', GalleryView.as_view(), name='gallery'),

    
    path('contact/', ContactView.as_view(), name='contact'),

    path('api/contact/', ContactMessageCreateAPIView.as_view(), name='contact-message'),
 
]