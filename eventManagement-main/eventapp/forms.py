from django import forms
from .models import Applicant

class EventForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['full_name', 'email', 'phone']
