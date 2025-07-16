from django.contrib import admin
from .models import (Service,CarCategory, Car, Booking, SpecialOffer,GreenRouteService,
                     SolutionService,TravelService,GreenLightService,GreenRouteContact,Testimonial)
# Register your models here.


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'is_featured', 'order')
    list_filter = ('service_type', 'is_featured')
    search_fields = ('name', 'short_description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CarCategory)
class CarCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']
    search_fields = ['name'] 


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'transmission', 'car_type', 'seats', 'rating', 'price_per_day', 'is_trending')
    list_filter = ('transmission', 'car_type', 'is_trending', 'category')
    search_fields = ('name',)
    autocomplete_fields = ['category']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'car', 'pickup_date', 'return_date', 'created_at')
    search_fields = ('customer_name',)
    list_filter = ('pickup_date', 'return_date', 'car')


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('car', 'discount_percentage', 'valid_from', 'valid_to', 'title')
    list_filter = ('valid_from', 'valid_to', 'car')



admin.site.register(GreenRouteService)

@admin.register(SolutionService)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'order')
    list_editable = ('order',)
    ordering = ('order',)

@admin.register(TravelService)
class TravelServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    ordering = ('order',)


admin.site.register(GreenLightService)
admin.site.register(GreenRouteContact)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company', 'rating', 'is_active', 'created_at')
    list_filter = ('is_active', 'rating')
    search_fields = ('full_name', 'company', 'message')

