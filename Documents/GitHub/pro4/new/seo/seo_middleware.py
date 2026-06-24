# seo_middleware.py
from django.urls import resolve
from .models import PageSEO
from django.core.cache import cache
import re

class SEOMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Only process HTML responses
        if 'text/html' in response.get('Content-Type', ''):
            try:
                # Get cached SEO or query database
                cache_key = f'seo_{request.path}'
                seo = cache.get(cache_key)
                if not seo:
                    seo = PageSEO.objects.get(url_path=request.path)
                    cache.set(cache_key, seo, 60*60)  # Cache for 1 hour
                
                content = response.content.decode('utf-8')
                
                # Replace title tag
                if seo.title:
                    content = re.sub(
                        r'<title>.*?</title>',
                        f'<title>{seo.title}</title>',
                        content
                    )
                
                # Add meta description
                if seo.meta_description:
                    meta_desc = f'<meta name="description" content="{seo.meta_description}">'
                    if '<meta name="description"' not in content:
                        # Insert if doesn't exist
                        content = content.replace('</title>', f'</title>\n{meta_desc}')
                
                # Add meta keywords
                if seo.meta_keywords:
                    meta_keywords = f'<meta name="keywords" content="{seo.meta_keywords}">'
                    if '<meta name="keywords"' not in content:
                        content = content.replace('</title>', f'</title>\n{meta_keywords}')
                
                # Add H1 tag
                if seo.h1_tag:
                    # Find existing H1 block
                    h1_block = re.search(r'{% block h1 %}.*?{% endblock %}', content)
                    if h1_block:
                        # Replace block content
                        content = content.replace(
                            h1_block.group(0),
                            f'{{% block h1 %}}<h1 class="seo-h1">{seo.h1_tag}</h1>{{% endblock %}}'
                        )
                    else:
                        # Insert before content block
                        content = content.replace(
                            '{% block content %}',
                            f'<h1 class="seo-h1">{seo.h1_tag}</h1>\n{{% block content %}}'
                        )
                
                response.content = content.encode('utf-8')
                
            except (PageSEO.DoesNotExist, UnicodeDecodeError):
                # No SEO record exists for this path or not HTML content
                pass
        
        return response