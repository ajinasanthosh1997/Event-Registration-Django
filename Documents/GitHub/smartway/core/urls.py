from django.urls import path
from .views import (HomeView,ContactMessageCreateAPIView,AboutView,ServiceView,
                    GalleryView,BlogsView,BlogDetailView,ContactView, BusinessCenterView,GreenLightServiceView,
                    TravelTourismView,RentACarView,SevenSolutionView,GreenRouteView)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),

    path('services/', ServiceView.as_view(), name='services'),

    path('services/business-center/', BusinessCenterView.as_view(), name='business_center'),
    path('services/green-light-service/', GreenLightServiceView.as_view(), name='green_light_service'),
    path('services/travel-tourism/', TravelTourismView.as_view(), name='travel_tourism'),
    path('services/rent-a-car/', RentACarView.as_view(), name='rent_a_car'),
    path('services/seven-solution/', SevenSolutionView.as_view(), name='seven_solution'),
    path('services/green-route/', GreenRouteView.as_view(), name='green_route'),

    path('gallery/', GalleryView.as_view(), name='gallery'),

    path('blogs/', BlogsView.as_view(), name='blogs'),
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-details'),
    
    path('contact/', ContactView.as_view(), name='contact'),

    path('api/contact/', ContactMessageCreateAPIView.as_view(), name='contact-message'),
]