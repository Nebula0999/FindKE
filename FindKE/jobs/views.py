from django.shortcuts import render
from rest_framework import viewsets
from .serializers import JobApplicationSerializer, JobPostingSerializer, MessageSerializer, JobAssignmentSerializer, JobCompletionSerializer
from .models import JobPosting, JobApplication, JobAssignment, JobCompletion, Message
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsClient, IsFreelancer, IsAdmin
from rest_framework.decorators import action
from rest_framework.response import Response


class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsClient, IsAdmin]
        else:
            permission_classes = [IsAuthenticated, IsClient, IsFreelancer, IsAdmin]
        return [permission() for permission in permission_classes]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsClient, IsAdmin]
        else:
            permission_classes = [IsAuthenticated, IsClient, IsFreelancer, IsAdmin]
        return [permission() for permission in permission_classes]

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsFreelancer, IsAdmin]
        else:
            permission_classes = [IsAuthenticated, IsClient, IsFreelancer, IsAdmin]
        return [permission() for permission in permission_classes]

class JobAssignmentViewSet(viewsets.ModelViewSet):
    queryset = JobAssignment.objects.all()
    serializer_class = JobAssignmentSerializer
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        job_assignment = self.get_object()
        if job_assignment.job_application.client != request.user:
            return Response({'error': 'You are not authorized to accept this job.'}, status=403)
        job_assignment.status = 'accepted'
        job_assignment.assigned_to = job_assignment.job_application.freelancer
        job_assignment.assignee = job_assignment.job_application.client
        job_assignment.save()
        return Response({'status': 'job accepted'})

class JobCompletionViewSet(viewsets.ModelViewSet):
    queryset = JobCompletion.objects.all()
    serializer_class = JobCompletionSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdmin]
        else:
            permission_classes = [IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]


