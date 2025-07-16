from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import (Service,CarCategory, Car, Booking, SpecialOffer,GreenRouteService,
                     SolutionService,TravelService,GreenLightService,GreenRouteContact,Testimonial)
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import GreenRouteContactSerializer
# Create your views here.


class ServiceView(ListView):
    model = Service
    template_name = 'core/services/services.html'
    context_object_name = 'services'
    ordering = ['order']  # Order by the 'order' field

    def get_queryset(self):
        # Get all services ordered by 'order' field
        return Service.objects.all().order_by('order')
    
class BusinessCenterView(TemplateView):
    template_name = 'core/services/business-center.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['footer'] = Service.objects.all().order_by('order')
        context['service'] = Service.objects.get(service_type='business_center')
        return context


class GreenLightServiceView(TemplateView):
    template_name = 'core/services/green-light-service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = Service.objects.get(service_type='green_light_service')
        context['services'] = GreenLightService.objects.all()
        context['footer'] = Service.objects.all().order_by('order')

        return context


class TravelTourismView(TemplateView):
    template_name = 'core/services/travel-tourism.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = Service.objects.get(service_type='travel_tourism')
        context['services'] = TravelService.objects.all()
        context['footer'] = Service.objects.all().order_by('order')
        return context


class RentACarView(TemplateView):
    template_name = "core/services/rent-a-car.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # existing
        context["service"] = Service.objects.get(service_type="rent_a_car")
        context['footer'] = Service.objects.all().order_by('order')
        # NEW ➜ all categories (use .prefetch_related for efficiency if you like)
        context["categories"] = CarCategory.objects.all()

        # NEW ➜ cars flagged as trending (limit to 4 to match your grid)
        context["trending_cars"] = (
            Car.objects.filter(is_trending=True).select_related("category")[:4]
        )

        # NEW ➜ today’s active offer (first match)
        today = timezone.localdate()
        context["active_offer"] = (
            SpecialOffer.objects
            .filter(valid_from__lte=today, valid_to__gte=today)
            .select_related("car")
            .first()
        )

        return context


class SevenSolutionView(TemplateView):
    template_name = 'core/services/seven-solution.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = Service.objects.get(service_type='seven_solution')  # Optional header section
        context['solutions'] = SolutionService.objects.all()  # All 7 solutions ordered by 'order'
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:3]
        context['footer'] = Service.objects.all().order_by('order')

        return context

class GreenRouteView(TemplateView):
    template_name = 'core/services/green-route.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = Service.objects.get(service_type='green_route')
        context['services'] = GreenRouteService.objects.all().order_by('order')
        context['footer'] = Service.objects.all().order_by('order')
        return context

@method_decorator(csrf_exempt, name='dispatch')
class GreenRouteContactCreateView(APIView):
    def post(self, request):
        serializer = GreenRouteContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Your message has been submitted successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)