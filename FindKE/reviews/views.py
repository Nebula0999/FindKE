from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ReviewSerializer
from .models import Review

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
