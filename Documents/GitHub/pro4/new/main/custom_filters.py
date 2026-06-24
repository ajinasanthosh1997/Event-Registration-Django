# In your Django app, create a templatetags directory (if not already present)
# Inside templatetags, create a file, e.g., my_filters.py
from django import template

register = template.Library()

@register.filter
def is_image_or_video(value):
    """
    Custom template filter to check if the file is an image or video based on its extension.
    """
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.mp4', '.mov', '.avi']
    ext = value.lower().rsplit('.', 1)[-1] if '.' in value else ''
    return ext in valid_extensions
