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
    
    class Meta:
        verbose_name = "Service Categories"
        verbose_name_plural = "Service Categories"

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



