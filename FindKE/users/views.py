from django.shortcuts import render
from .models import User, Client, Freelancer, Admin
from . serializers import UserSerializer, ClientSerializer, FreelancerSerializer, AdminSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.permissions import IsClient, IsFreelancer, IsAdmin

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsClient]
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class FreelancerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsFreelancer]
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer

class AdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

