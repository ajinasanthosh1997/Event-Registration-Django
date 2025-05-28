from django import forms
from .models import JewellerCategory, JewellerProduct

class JewellerCategoryForm(forms.ModelForm):
    class Meta:
        model = JewellerCategory
        fields = '__all__'

class JewellerProductForm(forms.ModelForm):
    class Meta:
        model = JewellerProduct
        fields = '__all__'
