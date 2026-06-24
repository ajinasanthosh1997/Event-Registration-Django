from django.contrib import admin
from .models import PageSEO

@admin.register(PageSEO)
class PageSEOAdmin(admin.ModelAdmin):
    list_display = ('url_path', 'title', 'created_at')
    search_fields = ('url_path', 'title')
    fieldsets = (
        ('Basic Information', {
            'fields': ('url_path', 'title', 'h1_tag', 'content', 'image_alt')
        }),
        ('Meta Tags', {
            'fields': ('meta_description', 'meta_keywords', 'robots', 'canonical_url')
        }),
        ('Social Media', {
            'fields': ('og_title', 'og_description', 'og_image')
        }),
        ('Verification', {
            'fields': ('verification_tag',),
            'classes': ('collapse',)
        }),
    )