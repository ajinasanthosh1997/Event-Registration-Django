from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    cpr = models.CharField(max_length=20, blank=True, null=True)

    TYPE_OF_REQUEST_CHOICES = [
        ('rent_car', 'Rent a car'),
        ('travel', 'Travel'),
        ('business_center', 'Business Center'),
    ]
    type_of_request = models.CharField(max_length=50, choices=TYPE_OF_REQUEST_CHOICES)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.get_type_of_request_display()}"



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class GalleryItem(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='gallery/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='gallery_items')
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def is_video(self):
        return self.media_type == 'video'
    
    def __str__(self):
        return self.title



class Author(models.Model):
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='authors/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField(blank=True, null=True) 
    content = RichTextField()
    image = models.ImageField(upload_to='blog_images/')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    featured = models.BooleanField(default=False)
    reading_time = models.PositiveIntegerField(help_text="Time in minutes", default=3)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def related_articles(self):
        return BlogPost.objects.filter(category=self.category).exclude(id=self.id)[:3]

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
    logo = models.ImageField(upload_to='services/logos/')
    short_description = models.TextField()
    features = models.JSONField(default=list)
    
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # Map service types to their URL names
        url_map = {
            'business_center': 'business_center',
            'green_light_service': 'green_light_service',
            'travel_tourism': 'travel_tourism',
            'rent_a_car': 'rent_a_car',
            'seven_solution': 'seven_solution',
            'green_route': 'green_route',
        }
        return reverse(url_map.get(self.service_type, 'services'))
    

class CarCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='car_categories/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class VehicleFeature(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('coupe', 'Coupe'),
        ('hatchback', 'Hatchback'),
        ('convertible', 'Convertible'),
        ('truck', 'Truck'),
        ('van', 'Van'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
        ('semi-automatic', 'Semi-Automatic'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    category = models.ForeignKey(CarCategory, on_delete=models.SET_NULL, null=True, related_name='vehicles')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    seats = models.PositiveIntegerField()
    image = models.ImageField(upload_to='vehicles/')
    rating = models.DecimalField(
        max_digits=2, 
        decimal_places=1, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    features = models.ManyToManyField(VehicleFeature, blank=True)
    is_trending = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class SpecialOffer(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    background_image = models.ImageField(upload_to='special_offers/')
    button_text = models.CharField(max_length=50, default='Book Now')
    button_link = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title