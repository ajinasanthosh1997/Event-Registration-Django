from .models import PageSEO
from django.core.cache import cache
from django.urls import resolve

def seo_context(request):
    cache_key = f'seo_{request.path}'
    seo = cache.get(cache_key)
    
    if not seo:
        try:
            seo = PageSEO.objects.get(url_path=request.path)
            cache.set(cache_key, seo, 60*60)  # Cache for 1 hour
        except PageSEO.DoesNotExist:
            seo = None
    
    return {
        'seo': seo,
        'canonical_url': seo.canonical_url if seo and seo.canonical_url else request.build_absolute_uri(request.path)
    }

