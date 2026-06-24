# main/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from main.models import Blog, Service
class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return [
            'main:index',
            'main:about',
            'main:work',
            'main:contact',
            'main:team',
            'main:blog',
            'main:gallery',
        ]

    def location(self, item):
        return reverse(item)

class ServiceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Service.objects.all()

    def location(self, obj):
        return reverse('main:service_details', args=[obj.slug])

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.publication_date


