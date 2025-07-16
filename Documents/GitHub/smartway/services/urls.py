from django.urls import path
from .views import (ServiceView,BusinessCenterView,GreenLightServiceView,
                    TravelTourismView,RentACarView,SevenSolutionView,GreenRouteView,GreenRouteContactCreateView)
app_name="services"

urlpatterns = [
    
    path('services/', ServiceView.as_view(), name='services'),

    path('services/business-center/', BusinessCenterView.as_view(), name='business_center'),
    path('services/green-light-service/', GreenLightServiceView.as_view(), name='green_light_service'),
    path('services/travel-tourism/', TravelTourismView.as_view(), name='travel_tourism'),
    path('services/rent-a-car/', RentACarView.as_view(), name='rent_a_car'),
    path('services/seven-solution/', SevenSolutionView.as_view(), name='seven_solution'),
    path('services/green-route/', GreenRouteView.as_view(), name='green_route'),

    path('api/greenroute-contact/', GreenRouteContactCreateView.as_view(), name='greenroute-contact'),
]