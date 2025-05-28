from django.db import models
from django.utils.text import slugify

class Jeweler(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='jeweller_images/', null=True, blank=True)
    phone = models.CharField(max_length=15)  # Updated to CharField for better phone number management
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class JewellerCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class JewellerProduct(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(JewellerCategory, on_delete=models.CASCADE, related_name='products')
    jeweller = models.ForeignKey(Jeweler, on_delete=models.CASCADE, related_name='products')
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Weight in grams
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
