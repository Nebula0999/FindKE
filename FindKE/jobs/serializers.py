from rest_framework.serializers import ModelSerializer
from . models import JobPosting, JobApplication, JobAssignment, JobCompletion, User, Message

class JobPostingSerializer(ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ['id', 'client', 'title', 'description', 'required_skills', 'budget', 'deadline', 'attachment']

class JobApplicationSerializer(ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'freelancer', 'job_posting', 'cover_letter', 'proposed_budget', 'status']

class JobAssignmentSerializer(ModelSerializer):
    class Meta:
        model = JobAssignment
        fields = ['job_application', 'assigned_date', 'completion_date', 'status', 'assigned_to', 'assignee']

class JobCompletionSerializer(ModelSerializer):
    class Meta:
        model = JobCompletion
        fields = ['job_assignment', 'rating', 'feedback', 'status', 'completed_by', 'completion_date']

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp']