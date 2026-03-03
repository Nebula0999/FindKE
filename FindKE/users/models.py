from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'client', 'Client'
        ADMIN = 'admin', 'Admin'
        FREELANCER = 'freelancer', 'Freelancer'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)
    skills = models.TextField(blank=True)
    rating = models.FloatField(default=0.0)

    db_table = 'users_user'
    indexes = [
        models.Index(fields=['email']),
        models.Index(fields=['name']),
        models.Index(fields=['role']),
    ]

    def __str__(self):
        return self.name

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    job_success_rate = models.FloatField(default=0.0)
    spending = models.FloatField(default=0.0)

    db_table = 'users_client'
    indexes = [
        models.Index(fields=['company_name']),
        models.Index(fields=['user']),
        models.Index(fields=['job_success_rate']),
    ]

    def __str__(self):
        return self.user.name
    
class Freelancer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio = models.TextField(blank=True)
    job_applications = models.ManyToManyField('jobs.JobPosting', blank=True)
    job_success_rate = models.FloatField(default=0.0)
    earnings = models.FloatField(default=0.0)

    db_table = 'users_freelancer'
    indexes = [
        models.Index(fields=['user']),
        models.Index(fields=['job_applications']),
        models.Index(fields=['job_success_rate']),
        models.Index(fields=['earnings']),
        ]
    def __str__(self):
        return self.user.name
    
class Admin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.name