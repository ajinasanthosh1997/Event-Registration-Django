from django.db import models
from django.core.validators import FileExtensionValidator
from PIL import Image
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
import os
from .mixins import WebPImageMixin
from django.conf import settings
from io import BytesIO
from django.core.files import File
from webpfield.fields import WebPField


# Updated WebPImageMixin (add to your mixins.py or keep here)
class WebPImageMixin:
    def convert_to_webp(self, image_field):
        img_path = image_field.path
        img_name, img_ext = os.path.splitext(image_field.name)
        
        # Skip if already WebP
        if img_ext.lower() == '.webp':
            return

        try:
            img = Image.open(img_path)
            
            # Convert to RGB if RGBA
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            
            # Create WebP in memory
            buffer = BytesIO()
            img.save(buffer, format='WEBP', quality=85)
            webp_filename = f"{img_name}.webp"
            
            # Save new file
            image_field.save(
                webp_filename,
                File(buffer),
                save=False
            )
            
            # Remove original file
            if os.path.exists(img_path):
                os.remove(img_path)
                
        except Exception as e:
            print(f"Error converting to WebP: {e}")


class WorkingRegion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ContactDetail(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    working_region = models.ForeignKey(WorkingRegion, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.email


class CustomerMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = CKEditor5Field(config_name='default')

    def __str__(self):
        return self.question

class Logo(WebPImageMixin, models.Model):
    CAROUSEL_GROUP_CHOICES = (
        (1, 'Carousel 1'),
        (2, 'Carousel 2'),
        (3, 'Carousel 3'),
    )
    
    name = models.CharField(max_length=100)
    logo =WebPField(upload_to='logos/')
        
    carousel_group = models.PositiveSmallIntegerField(
        choices=CAROUSEL_GROUP_CHOICES,
        default=1,
        help_text="Select which carousel this logo should appear in"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.logo:
            img = Image.open(self.logo.path)
            max_height, max_width = 200, 300
            if img.height > max_height or img.width > max_width:
                img.thumbnail((max_width, max_height))
                img.save(self.logo.path)
         


class LogoSecond(WebPImageMixin, models.Model):
    name = models.CharField(max_length=100)
    logo = WebPField(
        upload_to='logos_second/')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.logo:
            img = Image.open(self.logo.path)
            max_height, max_width = 200, 300
            if img.height > max_height or img.width > max_width:
                img.thumbnail((max_width, max_height))
                img.save(self.logo.path)
        


class LogoThird(WebPImageMixin, models.Model):
    name = models.CharField(max_length=100)
    logo = WebPField(upload_to='logos_third/')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.logo:
            img = Image.open(self.logo.path)
            max_height, max_width = 200, 300
            if img.height > max_height or img.width > max_width:
                img.thumbnail((max_width, max_height))
                img.save(self.logo.path)
            



class About(models.Model):
    title = models.CharField(max_length=100)
    description = CKEditor5Field(config_name='default')

    def __str__(self):
        return self.title


class Work(models.Model):
    title = models.CharField(max_length=100)
    media = models.FileField(
        upload_to='work_media/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'webp', 'mp4', 'mov', 'avi'])]
    )
    description = CKEditor5Field(config_name='default')
    division = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='works')
   

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.media.name.lower().endswith(('jpg', 'png', 'jpeg', 'webp')):
            img = Image.open(self.media.path)
            max_height, max_width = 300, 500
            if img.height > max_height or img.width > max_width:
                img.thumbnail((max_width, max_height))
                img.save(self.media.path)
       


class WorkScreenshot(WebPImageMixin, models.Model):
    work = models.ForeignKey(Work, related_name='screenshots', on_delete=models.CASCADE)
    image = WebPField(upload_to='screenshots/')
   
    order = models.PositiveIntegerField(default=0)
    show_on_home = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.work.title} - Screenshot {self.id}"


   


class FeaturedWork(models.Model):
    work = models.OneToOneField(Work, on_delete=models.CASCADE, related_name='featured')
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers show first)")
    additional_media = models.FileField(
        upload_to='featured_work/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'webp', 'mp4', 'mov', 'avi'])],
        blank=True,
        null=True
    )
   

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Featured: {self.work.title}"

    


class Testimonial(WebPImageMixin, models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    text = CKEditor5Field(config_name='default')
    logo = WebPField(upload_to='testimonials/logos/')
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f"{self.name} - {self.brand}"


       

class Blog(WebPImageMixin, models.Model):
    title = models.CharField(max_length=100)
    content = CKEditor5Field(null=True)
    publication_date = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=50)
    image =WebPField(upload_to='blog_images/')
   
    date = models.DateField(null=True)
    is_featured = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
  
      

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:blog-detail', args=[self.slug])


class TeamImage(WebPImageMixin,models.Model):
    image = WebPField(
        upload_to='team_image/'
    )
  
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            max_height = 500
            max_width = 1400
            if img.height > max_height or img.width > max_width:
                output_size = (max_width, max_height)
                img.thumbnail(output_size)
                img.save(self.image.path)
          
       


class CEO(WebPImageMixin,models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    description = CKEditor5Field(config_name='default', blank=True, null=True)
    image = WebPField(upload_to='team_images/', blank=True, null=True)
   
    is_ceo = models.BooleanField(default=False)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    x = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name or "Unnamed CEO"
    

   


class TeamMember(WebPImageMixin,models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    image = WebPField(upload_to='team_images/', blank=True, null=True)
   
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    x = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name or "Unnamed Team Member"
    
    def save(self, *args, **kwargs):
        """
        Revised save method to handle WebP conversion safely.
        """
        # First, save the model to get a PK and make the file available
        super().save(*args, **kwargs)

        # Check if the image field has a file and needs conversion
        if self.image: # Replace 'logo' with your specific ImageField name
            img = Image.open(self.logo.path)
            
            # Perform resizing first, if needed
            max_height, max_width = 200, 300
            if img.height > max_height or img.width > max_width:
                img.thumbnail((max_width, max_height))
                # Save the resized version temporarily
                img.save(self.image.path)
            
    
      


class Service(WebPImageMixin,models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    image = WebPField(upload_to='service_images/')
   
    icon = WebPField(upload_to='service_icons/', null=True, blank=True)
  
    content = CKEditor5Field(config_name='default')
    subcontent = CKEditor5Field(config_name='default', null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Revised save method to handle WebP conversion safely.
        """
        # First, save the model to get a PK and make the file available
        super().save(*args, **kwargs)

        # Check if the image field has a file and needs conversion
        if self.image: # Replace 'logo' with your specific ImageField name
            img = Image.open(self.image.path)
            
            # Perform resizing first, if needed
            max_height, max_width = 200, 300
            if img.height > max_height or img.width > max_width:
                img.thumbnail((max_width, max_height))
                # Save the resized version temporarily
                img.save(self.image.path)
            
          
        

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('main:service_details', args=[self.slug])


class SubService(WebPImageMixin,models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    icon = WebPField(upload_to='icons/')

    name = models.CharField(max_length=100)
    content = CKEditor5Field(config_name='default')

    def save(self, *args, **kwargs):
        """
        Revised save method to handle WebP conversion safely.
        """
        # First, save the model to get a PK and make the file available
        super().save(*args, **kwargs)

        # Check if the image field has a file and needs conversion
        if self.icon: # Replace 'logo' with your specific ImageField name
            img = Image.open(self.icon.path)
            
            # Perform resizing first, if needed
            max_height, max_width = 200, 300
            if img.height > max_height or img.width > max_width:
                img.thumbnail((max_width, max_height))
                # Save the resized version temporarily
                img.save(self.icon.path)
            
          
       

    def __str__(self):
        return self.name
    

class HomePageVideo(models.Model):
    video = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video {self.pk}"


class Project(WebPImageMixin,models.Model):
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    image = WebPField(upload_to='projects/')
   
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
      
      
    

class ProjectsDone(models.Model):
    number=models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Story(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = CKEditor5Field(config_name='default')
    date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Story, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class StoryImage(models.Model):
    story = models.ForeignKey(Story, related_name='images', on_delete=models.CASCADE)
    image = WebPField(upload_to='stories/images/')
    

    def __str__(self):
        return f"Image for {self.story.title}"
    
 


class GalleryGroup(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the gallery group")
    description = CKEditor5Field(config_name='default', blank=True, help_text="Optional description for the group")
    is_featured = models.BooleanField(default=False, help_text="Mark this group as featured")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Gallery Group'
        verbose_name_plural = 'Gallery Groups'


class GalleryImage(WebPImageMixin,models.Model):
    group = models.ForeignKey(GalleryGroup, related_name='images', on_delete=models.CASCADE)
    image = WebPField(upload_to='gallery/large/')
   
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.group.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.convert_to_webp(self.image)
        


class NavbarItem(models.Model):
    label = models.CharField(max_length=100)
    url_name = models.CharField(max_length=100)
    anchor = models.CharField(max_length=100, blank=True, null=True)
    parameters = models.JSONField(blank=True, null=True)
    order = models.PositiveIntegerField(
        default=0, 
        help_text="Display order (lower numbers show first)"
    )

    class Meta:
        ordering = ['order', 'label']  # Order by order field, then by label as tiebreaker

    def get_url(self):
        url = reverse(self.url_name, kwargs=self.parameters or {})
        if self.anchor:
            url += f"#{self.anchor}"
        return url

    def __str__(self):
        return self.label

class MethodStep(models.Model):
    STEP_NUMBERS = [
        (1, 'Step 1'),
        (2, 'Step 2'),
        (3, 'Step 3'),
        (4, 'Step 4'),
        (5, 'Step 5'),
    ]
    
    step_number = models.IntegerField(choices=STEP_NUMBERS, unique=True)
    title = models.CharField(max_length=100)
    description = CKEditor5Field(config_name='default')
    image = WebPField(upload_to='method_images/')
    
    class Meta:
        ordering = ['step_number']  # Ensures consistent ordering
    
    def __str__(self):
        return f"{self.step_number}. {self.title}"
