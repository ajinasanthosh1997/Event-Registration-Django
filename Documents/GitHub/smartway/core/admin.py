from django.contrib import admin
from .models import ContactMessage,Author, BlogCategory, Tag, BlogPost,Category, GalleryItem,Service
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import format_html
# Register your models here.


admin.site.register(ContactMessage)

class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    description = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = BlogPost
        fields = '__all__'

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ['title', 'author', 'category', 'featured', 'created_at']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Author)
admin.site.register(BlogCategory)
admin.site.register(Tag)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_count')
    search_fields = ('name',)
    
    def item_count(self, obj):
        return obj.gallery_items.count()
    item_count.short_description = 'Items'

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'category', 'file_preview', 'created_at')
    list_filter = ('media_type', 'category', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('file_preview',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'description', 'media_type')
        }),
        ('Media', {
            'fields': ('file', 'file_preview')
        }),
    )
    
    def file_preview(self, obj):
        if obj.file:
            if obj.media_type == 'image':
                return mark_safe(f'<img src="{obj.file.url}" style="max-height: 100px; max-width: 150px;" />')
            else:  # video
                return mark_safe(
                    f'<div style="position:relative; max-height:100px; max-width:150px;">'
                    f'<video style="max-height:100px; max-width:150px; object-fit:cover;">'
                    f'<source src="{obj.file.url}" type="video/mp4">'
                    f'</video>'
                    f'<div style="position:absolute; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.3); display:flex; align-items:center; justify-content:center;">'
                    f'<svg style="width:24px; height:24px; color:white;" fill="currentColor" viewBox="0 0 24 24">'
                    f'<path d="M8 5v14l11-7z" />'
                    f'</svg>'
                    f'</div>'
                    f'</div>'
                )
        return "No File"
    file_preview.short_description = 'Preview'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'is_featured', 'order')
    list_filter = ('service_type', 'is_featured')
    search_fields = ('name', 'short_description')
    prepopulated_fields = {'slug': ('name',)}