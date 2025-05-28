from django import forms
from main.models import *
from jeweller.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'gold_purity', 'metal_color', 'weight', 'price_range', 'product_video', 'product_code', 'image', 'jeweller','slug']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'gold_purity': forms.Select(attrs={'class': 'form-control'}),
            'metal_color': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.TextInput(attrs={'class': 'form-control'}),
            'price_range': forms.TextInput(attrs={'class': 'form-control'}),
            'product_video': forms.TextInput(attrs={'class': 'form-control'}),
            'product_code': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'jeweller': forms.Select(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductSpecsForm(forms.ModelForm):
    class Meta:
        model = ProductSpecs
        fields = ['stone_type', 'jeweller', 'category', 'metal_purity_details', 'wearing_style', 'metal_color', 'occasion','slug']
        widgets = {
            'stone_type': forms.Select(attrs={'class': 'form-control'}),
            'jeweller': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'metal_purity_details': forms.Select(attrs={'class': 'form-control'}),
            'wearing_style': forms.TextInput(attrs={'class': 'form-control'}),
            'metal_color': forms.Select(attrs={'class': 'form-control'}),
            'occasion': forms.Select(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductDescriptionForm(forms.ModelForm):
    class Meta:
        model = ProductDescription
        fields = ['content','slug']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent','slug']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['quote', 'rating', 'review','slug']

class JewellerForm(forms.ModelForm):
    class Meta:
        model = Jeweller
        fields = ['name', 'location', 'image', 'phone','slug']

class JewelleryForm(forms.ModelForm):
    class Meta:
        model = Jeweler
        fields = ['name', 'location', 'image', 'phone','slug']


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))

    class Meta:
        model = CustomUser
        fields = ['email', 'password']