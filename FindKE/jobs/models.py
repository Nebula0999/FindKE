from django.db import models
from users.models import User
import uuid
    
class JobPosting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField()
    budget = models.FloatField()
    deadline = models.DateField()
    attachment = models.FileField(upload_to='job_attachments/', null=True, blank=True)

    db_table = 'job_postings'
    indexes = [
        models.Index(fields=['client']),
        models.Index(fields=['title']),
        models.Index(fields=['required_skills']),
    ]
    def __str__(self):
        return self.title

class JobApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_applications')
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField()
    proposed_budget = models.FloatField()
    status = models.CharField(max_length=20, default='PENDING')

    db_table = 'job_applications'
    indexes = [
        models.Index(fields=['freelancer']),
        models.Index(fields=['job_posting']),
        models.Index(fields=['status']),
    ]
    def __str__(self):
        return f"{self.freelancer.name} - {self.job_posting.title}"
    

class JobAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_application = models.OneToOneField(JobApplication, on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='ASSIGNED')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_jobs', null=True, blank=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_jobs_as_client', null=True, blank=True)

    db_table = 'job_assignment'
    indexes = [
        models.Index(fields=['job_application']),
        models.Index(fields=['status']),
        models.Index(fields=['assigned_to']),
        models.Index(fields=['assignee']),
    ]
    def __str__(self):
        return f"{self.job_application.freelancer.name} - {self.job_application.job_posting.title}"
    
class JobCompletion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_assignment = models.OneToOneField(JobAssignment, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    completed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_jobs', null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='COMPLETED')
    completion_date = models.DateField(auto_now_add=True)

    db_table = 'job_completion'
    indexes = [
        models.Index(fields=['job_assignment']),
        models.Index(fields=['status']),
        models.Index(fields=['completed_by']),
        models.Index(fields=['completion_date']),
    ]
    def __str__(self):
        return f"{self.job_assignment.job_application.freelancer.name} - {self.job_assignment.job_application.job_posting.title}"
    
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    db_table = 'jobs_message'
    indexes = [
        models.Index(fields=['sender']),
        models.Index(fields=['recipient']),
        models.Index(fields=['job']),
    ]
    def __str__(self):
        return f"{self.sender.name} to {self.recipient.name} at {self.timestamp}"
    
