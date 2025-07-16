from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from django.views.generic import ListView, DetailView, TemplateView
from .models import Category, GalleryItem
from services.models import Service


class ContactMessageCreateAPIView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Message submitted successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeView(TemplateView):
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all().order_by('order')
        return context
    
    

class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all().order_by('order')
        return context


class GalleryView(TemplateView):
    template_name = 'core/gallery.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all().order_by('order')
        # Get all categories
        context['categories'] = Category.objects.all()
        
        
        # Filter gallery items by category if specified
        gallery_items = GalleryItem.objects.all()
        category_id = self.request.GET.get('category')
        if category_id:
            gallery_items = gallery_items.filter(category__id=category_id)
        
        context['gallery_items'] = gallery_items
        return context




class ContactView(TemplateView):
    template_name = 'core/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all().order_by('order')
        return context

