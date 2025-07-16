from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import BlogCategory,BlogPost
from services.models import Service
# Create your views here.



class BlogsView(ListView):
    template_name = 'core/blogs/blogs.html'
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
        context['services'] = Service.objects.all().order_by('order')
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
    template_name = 'core/blogs/blog_details.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all().order_by('order')
        context['related_articles'] = BlogPost.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context
    
    