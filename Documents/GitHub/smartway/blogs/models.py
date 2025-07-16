from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


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