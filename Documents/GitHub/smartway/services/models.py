from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.


class Service(models.Model):
    SERVICE_CHOICES = [
        ('business_center', 'Business Center'),
        ('green_light_service', 'Green Light Service'),
        ('travel_tourism', 'Travel & Tourism'),
        ('rent_a_car', 'Rent A Car'),
        ('seven_solution', 'Seven Solution'),
        ('green_route', 'Green Route'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    
    logo = models.ImageField(upload_to='services/logos/', help_text="Upload the service logo (icon style).")
    image = models.ImageField(upload_to='services/images/', blank=True, null=True, help_text="Upload a banner/cover image.")

    short_description = models.TextField()
    features = models.TextField(help_text="Enter features separated by line breaks")
    
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_feature_list(self):
        return [feature.strip() for feature in self.features.splitlines() if feature.strip()]
    
    def get_absolute_url(self):
        url_map = {
            'business_center': 'services:business_center',
            'green_light_service': 'services:green_light_service',
            'travel_tourism': 'services:travel_tourism',
            'rent_a_car': 'services:rent_a_car',
            'seven_solution': 'services:seven_solution',
            'green_route': 'services:green_route',
        }
        return reverse(url_map.get(self.service_type, 'services:services'))
  
    
class CarCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]

    TYPE_CHOICES = [
        ('suv', 'SUV'),
        ('luxury', 'Luxury'),
        ('sports', 'Sports'),
        ('premium', 'Premium'),
    ]

    name = models.CharField(max_length=100)
    category = models.ForeignKey(CarCategory, on_delete=models.CASCADE, related_name='cars')
    image = models.ImageField(upload_to='cars/')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    car_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    seats = models.PositiveSmallIntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    is_trending = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=100)
    pickup_date = models.DateField()
    return_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.car.name}"


class SpecialOffer(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='special_offers')
    discount_percentage = models.PositiveIntegerField()
    valid_from = models.DateField()
    valid_to = models.DateField()
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Offer for {self.car.name} ({self.discount_percentage}% off)"

class GreenRouteService(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    icon_svg = models.ImageField(upload_to='icon/',blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Green Route Service"
        verbose_name_plural = "Green Route Services"

    def __str__(self):
        return self.title

class SolutionService(models.Model):
    COLOR_CHOICES = [
        ('cyan', 'Cyan'),
        ('orange', 'Orange'),
        # Add more if needed
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_svg = models.ImageField(upload_to='icons/', blank=True, help_text="Upload an SVG/PNG icon")
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='cyan')
    features = models.TextField(help_text="Enter features separated by line breaks")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Seven Solution"
        verbose_name_plural = "Seven Solution Services"

    def __str__(self):
        return self.title

    def get_feature_list(self):
        return [feature.strip() for feature in self.features.splitlines() if feature.strip()]


class TravelService(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_image = models.ImageField(upload_to='services/icons/')  # Upload icon image here
    color = models.CharField(max_length=30, default='orange')  # Tailwind color prefix
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class GreenLightService(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_image = models.ImageField(upload_to='greenlight/icons/')
    button_text = models.CharField(max_length=50, default='Learn More')
    features = models.TextField(help_text="Enter features separated by line breaks")
    gradient_from = models.CharField(max_length=30, default='green-500')
    gradient_to = models.CharField(max_length=30, default='orange-500')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_feature_list(self):
        return [feature.strip() for feature in self.features.splitlines() if feature.strip()]
    

class GreenRouteContact(models.Model):
    SERVICE_CHOICES = [
        ('Freight Forwarding', 'Freight Forwarding'),
        ('Supply Chain Solutions', 'Supply Chain Solutions'),
        ('Warehousing Services', 'Warehousing Services'),
        ('Distribution Network', 'Distribution Network'),
        ('Other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service_needed = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service_needed}"

class SevenSolutionTestimonial(models.Model):
    STAR_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]

    full_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(choices=STAR_CHOICES, default=5)
    message = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.company})"

    class Meta:
        ordering = ['-created_at']

class Testimonial(models.Model):
    STAR_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]

    full_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(choices=STAR_CHOICES, default=5)
    message = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.company})"

    class Meta:
        ordering = ['-created_at']

