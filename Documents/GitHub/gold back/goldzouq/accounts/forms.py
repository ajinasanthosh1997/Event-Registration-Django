# forms.py
from django import forms
from .models import *

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'phone_number', 'location']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'log-in', 'placeholder': 'Enter your name'}),
            'phone_number': forms.NumberInput(attrs={'class': 'log-in', 'placeholder': 'Enter your phone number'}),
            'email': forms.EmailInput(attrs={'class': 'log-in', 'placeholder': 'Enter your mail ID'}),
            'location': forms.TextInput(attrs={'class': 'log-in', 'placeholder': 'Enter your location'}),
        }


class EmailLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'log-in', 'placeholder': 'Enter your mail ID'}))        

class PhoneLoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,  # adjust the max length based on your requirements
        widget=forms.TextInput(attrs={'class': 'log-in', 'placeholder': 'Enter your Phone number'}),
    )

class OTPForm(forms.Form):
    otp = forms.CharField(widget=forms.TextInput(attrs={'class': 'log-in', 'placeholder': 'Enter OTP'}))    


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser 
        fields = ['name', 'email', 'phone_number', 'location']    