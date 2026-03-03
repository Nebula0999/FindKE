from django.db import models
from users.models import User
from jobs.models import JobCompletion, JobPosting
import uuid

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='reviews')
    job_completion = models.OneToOneField(JobCompletion, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=0, blank=True)  # Rating out of 5
    feedback = models.TextField(blank=True)

    db_table = 'reviews_review'
    indexes = [
        models.Index(fields=['reviewer']),
        models.Index(fields=['reviewee']),
        models.Index(fields=['rating']),
    ]

    def __str__(self):
        return f"Review by {self.reviewer.name} for {self.reviewee.name}"
