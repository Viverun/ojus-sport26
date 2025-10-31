from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Student(AbstractUser):
    moodleID = models.IntegerField(unique=True, primary_key=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True)
    is_prohibited = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.username} ({self.moodleID})"