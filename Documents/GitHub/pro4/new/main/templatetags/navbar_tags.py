from django import template
from main.models import NavbarItem

register = template.Library()

@register.simple_tag
def get_navbar_items():
    return NavbarItem.objects.all()
