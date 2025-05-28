from django.db import models
from django.utils.text import slugify

class Jeweller(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='jeweller_images/', null=True, blank=True)
    phone = models.IntegerField()
    email = models.EmailField()
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)  # Add this line

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)  # Add this line

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('kids', 'Kids'),
        ('newborn', 'New Born'),
    ]
    GOLD_PURITY_CHOICES = [
        ('gold24CT', '24 CT'),
        ('gold22CT', '22 CT'),
        ('gold18CT', '18 CT'),
        ('gold14CT', '14 CT'),
        ('gold95CT', '95.00 CT'),
    ]
    METAL_COLOR_CHOICES = [
        ('white', 'White'),
        ('rose', 'Rose'),
        ('yellow', 'Yellow'),
        ('dualTone', 'Dual Tone'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    gold_purity = models.CharField(max_length=10, choices=GOLD_PURITY_CHOICES, null=True)
    metal_color = models.CharField(max_length=10, choices=METAL_COLOR_CHOICES, null=True)
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=3)
    price_range = models.CharField(max_length=50, null=True)
    product_video = models.URLField(null=True, blank=True)
    product_code = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    jeweller = models.ForeignKey(Jeweller, on_delete=models.CASCADE, related_name='products', null=True)
    slug = models.SlugField(unique=True, blank=True)
    downloadable_photo = models.FileField(upload_to='downloadable_photos/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductSpecs(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='specs')
    STONE_TYPE_CHOICES = [
        ('none', 'No stone available'),
        ('diamond', 'Diamond'),
        ('ruby', 'Ruby'),
        ('sapphire', 'Sapphire'),
        ('emerald', 'Emerald'),
    ]
    JEWELLER_CHOICES = [
        ('brand1', 'Chungath Jewellery'),
        ('brand2', 'Jos Jewellery'),
        ('brand3', 'Vellanikaran Gold and Diamonds'),
        ('brand4', 'Akkara Jewellers'),
        ('brand5', 'Mahila Jewellers'),
    ]
    METAL_PURITY_CHOICES = [
        ('gold24CT', '24 CT'),
        ('gold22CT', '22 CT'),
        ('gold18CT', '18 CT'),
        ('gold14CT', '14 CT'),
        ('gold95CT', '95.00 CT'),
    ]
    METAL_COLOR_CHOICES = [
        ('white', 'White'),
        ('rose', 'Rose'),
        ('yellow', 'Yellow'),
        ('dualTone', 'Dual Tone'),
    ]
    OCCASION_CHOICES = [
        ('daily_wear', 'Daily Wear'),
        ('wedding', 'Wedding'),
        ('party', 'Party'),
        ('casual', 'Casual'),
        ('formal', 'Formal'),
    ]

    stone_type = models.CharField(max_length=50, choices=STONE_TYPE_CHOICES, default='none')
    jeweller = models.ForeignKey(Jeweller, on_delete=models.CASCADE, related_name='product', null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    metal_purity_details = models.CharField(max_length=50, choices=METAL_PURITY_CHOICES, default='22ct')
    wearing_style = models.CharField(max_length=50, default='Daily Wear')
    metal_color = models.CharField(max_length=10, choices=Product.METAL_COLOR_CHOICES, default='yellow')
    occasion = models.CharField(max_length=50, choices=OCCASION_CHOICES, default='daily_wear')
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)  # Add this line

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Specs for {self.product.name}"

class ProductDescription(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='desc')
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)  # Add this line

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product.name)
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"Description for {self.product.name}"

class Store(models.Model):
    store_name = models.CharField(max_length=100)
    contact_person_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    website_or_instagram = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    email = models.EmailField()
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)  # Add this line

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.store_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.store_name

class Testimonial(models.Model):
    quote = models.TextField()
    rating = models.IntegerField(default=5)  # Assuming default rating is 5 stars
    review = models.CharField(max_length=500, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)  # Add this line

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.quote[:50])  # Create a slug from the first 50 characters of the quote
        super().save(*args, **kwargs)

    def __str__(self):
        return self.quote