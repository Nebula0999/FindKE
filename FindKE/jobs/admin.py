from django.contrib import admin
from .models import JobApplication, JobPosting, Message, JobAssignment, JobCompletion

admin.site.register(JobApplication)
admin.site.register(JobPosting)
admin.site.register(Message)
admin.site.register(JobAssignment)
admin.site.register(JobCompletion)
# Register your models here.
