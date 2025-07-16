from rest_framework import serializers
from .models import GreenRouteContact

class GreenRouteContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = GreenRouteContact
        fields = '__all__'