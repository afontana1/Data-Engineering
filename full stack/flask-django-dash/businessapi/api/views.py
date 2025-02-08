from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BusinessSerializer
from .models import Business

# Create your views here.
class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        qs = Business.objects.all()
        serializer = BusinessSerializer(qs, many=True)
        return Response(serializer.data)