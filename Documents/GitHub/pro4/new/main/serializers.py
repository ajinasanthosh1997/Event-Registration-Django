# serializers.py

from rest_framework import serializers
from .models import ContactDetail, CustomerMessage

class ContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetail
        fields = ['working_regions', 'phone', 'email']

class CustomerMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerMessage
        fields = ['id', 'name', 'email', 'message', 'created_on']
