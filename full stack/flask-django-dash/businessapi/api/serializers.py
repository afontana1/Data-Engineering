from rest_framework import serializers
from .models import Business

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = (
            'name', 'no_of_employees'
        )