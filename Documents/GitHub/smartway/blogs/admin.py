from django.contrib import admin
from django.contrib import admin
from .models import Author, BlogCategory, Tag, BlogPost
from ckeditor.widgets import CKEditorWidget
from django import forms


# Register your models here.
class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    description = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = BlogPost
        fields = '__all__'

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ['title', 'author', 'category', 'featured', 'created_at']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Author)
admin.site.register(BlogCategory)
admin.site.register(Tag)
