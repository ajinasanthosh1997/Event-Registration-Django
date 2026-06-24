from django.contrib import admin
from django.utils.html import strip_tags
from .models import *

# Register your models here.
admin.site.register(HomePageVideo)
admin.site.register(Logo)
admin.site.register(LogoSecond)
admin.site.register(LogoThird)
admin.site.register(About)
admin.site.register(Testimonial)
admin.site.register(Blog)
admin.site.register(TeamImage)
admin.site.register(CEO)
admin.site.register(TeamMember)
admin.site.register(Project)
admin.site.register(ProjectsDone)
admin.site.register(FAQ)
admin.site.register(WorkingRegion)
admin.site.register(ContactDetail)
admin.site.register(CustomerMessage)

@admin.register(NavbarItem)
class NavbarItemAdmin(admin.ModelAdmin):
    list_display = ('label', 'url_name', 'order')
    list_editable = ('order',)  # Allows editing order directly from list view
    ordering = ('order',)

@admin.register(FeaturedWork)
class FeaturedWorkAdmin(admin.ModelAdmin):
    list_display = ('work', 'order')
    list_editable = ('order',)
    search_fields = ('work__title',)
    




class SubServiceInline(admin.TabularInline):
    model = SubService
    extra = 1  # Number of empty subservice forms to display

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = [SubServiceInline]
    list_display = ( 'name','number', 'slug', 'content_short', 'subcontent_short')
    search_fields = ('name', 'number')
    list_filter = ('name',)
  
    fields = (
        'number', 'name', 'image', 'content', 'subcontent', 'slug'
    )

    def content_short(self, obj):
        content = strip_tags(obj.content or '')
        return content[:50] + '...' if len(content) > 50 else content
    content_short.short_description = 'Content'

    def subcontent_short(self, obj):
        content = strip_tags(obj.subcontent or '')
        return content[:50] + '...' if len(content) > 50 else content
    subcontent_short.short_description = 'Subcontent'

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1

@admin.register(GalleryGroup)
class GalleryGroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'created_at']
    inlines = [GalleryImageInline]

class WorkScreenshotInline(admin.TabularInline):
    model = WorkScreenshot
    extra = 1

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    inlines = [WorkScreenshotInline]
    list_display = ['title', 'display_division', 'description_short']
    list_filter = ('division',)
    search_fields = ('title', 'division__name', 'description')
    
    def display_division(self, obj):
        return obj.division.name if obj.division else "No Division"
    display_division.short_description = 'Division'
    
    def description_short(self, obj):
        description = strip_tags(obj.description or '')
        return description[:50] + '...' if len(description) > 50 else description
    description_short.short_description = 'Description'

@admin.register(MethodStep)
class MethodStepAdmin(admin.ModelAdmin):
    list_display = ['step_number', 'title', 'description_short']
    list_editable = ['title']

    def description_short(self, obj):
        description = strip_tags(obj.description or '')
        return description[:50] + '...' if len(description) > 50 else description
    description_short.short_description = 'Description'
