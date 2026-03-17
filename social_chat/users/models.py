from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['username'], name='username_idx'),
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['first_name', 'last_name'], name='name_idx'),
        ]

    def __str__(self):
        return self.username


