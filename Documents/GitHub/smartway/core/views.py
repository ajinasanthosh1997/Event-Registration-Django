from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from django.views.generic import ListView, DetailView, TemplateView
from .models import (BlogPost, BlogCategory, Tag, Author,Category, GalleryItem,Service,
                     CarCategory, VehicleFeature, Vehicle, SpecialOffer)

class ContactMessageCreateAPIView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Message submitted successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeView(TemplateView):
    template_name = 'core/index.html'

class AboutView(TemplateView):
    template_name = 'core/about.html'



class GalleryView(TemplateView):
    template_name = 'core/gallery.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all categories
        context['categories'] = Category.objects.all()
        
        # Filter gallery items by category if specified
        gallery_items = GalleryItem.objects.all()
        category_id = self.request.GET.get('category')
        if category_id:
            gallery_items = gallery_items.filter(category__id=category_id)
        
        context['gallery_items'] = gallery_items
        return context



class BlogsView(ListView):
    template_name = 'core/blogs.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = BlogPost.objects.prefetch_related('tags').select_related('author', 'category').order_by('-created_at')
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['categories'] = BlogCategory.objects.all()
        
        context['featured_article'] = BlogPost.objects.filter(featured=True).first()
        
        if context['featured_article']:
            context['latest_stories'] = BlogPost.objects.exclude(
                id=context['featured_article'].id
            ).order_by('-created_at')[:3]
        else:
            context['latest_stories'] = BlogPost.objects.order_by('-created_at')[:3]
        
        business_category = BlogCategory.objects.filter(name='Business').first()
        if business_category:
            context['business_highlights'] = BlogPost.objects.filter(
                category=business_category
            ).exclude(id=context['featured_article'].id if context['featured_article'] else None)[:2]
        
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'core/blog_details.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_articles'] = BlogPost.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context
    


class ContactView(TemplateView):
    template_name = 'core/contact.html'

class ServiceView(ListView):
    model = Service
    template_name = 'core/services.html'
    context_object_name = 'services'
    ordering = ['order']  # Order by the 'order' field

    def get_queryset(self):
        # Get all services ordered by 'order' field
        return Service.objects.all().order_by('order')
    
class BusinessCenterView(TemplateView):
    template_name = 'core/business-center.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = Service.objects.get(service_type='business_center')
        return context


class GreenLightServiceView(TemplateView):
    template_name = 'core/green-light-service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = Service.objects.get(service_type='green_light_service')
        return context


class TravelTourismView(TemplateView):
    template_name = 'core/travel-tourism.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = Service.objects.get(service_type='travel_tourism')
        return context


class RentACarView(TemplateView):
    template_name = 'core/rent-a-car.html'

  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = Service.objects.get(service_type='rent_a_car')
        context['categories'] = CarCategory.objects.filter(is_active=True).order_by('order')
        context['trending_vehicles'] = Vehicle.objects.filter(is_trending=True).order_by('order')[:4]
        context['special_offer'] = SpecialOffer.objects.filter(is_active=True).first()
        return context


class SevenSolutionView(TemplateView):
    template_name = 'core/seven-solution.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = Service.objects.get(service_type='seven_solution')
        return context


class GreenRouteView(TemplateView):
    template_name = 'core/green-route.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = Service.objects.get(service_type='green_route')
        return context