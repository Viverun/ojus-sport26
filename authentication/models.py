from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.

## to cahnge moodle to be identifier rather than username
class StudentManager(BaseUserManager):
    use_in_migrations = True

    # overriding a builting method
    def _create_user(self, moodleID, password, **extra_fields):
        if not moodleID:
            raise ValueError('The given moodleID must be set')
        
        user = self.model(moodleID=moodleID, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, moodleID, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(moodleID, password, **extra_fields)

    def create_superuser(self, moodleID, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(moodleID, password, **extra_fields)
    
class Student(AbstractUser):
    YEAR_CHOICES = [
        ('FE', 'First Year (FE)'),
        ('SE', 'Second Year (SE)'),
        ('TE', 'Third Year (TE)'),
        ('BE', 'Fourth Year (BE)'),
    ]
    BRANCH_CHOICES = [
        ('COMPS', 'Computer Engineering'),
        ('IT', 'Information Technology'),
        ('AIML', 'CSE Artifical Intelligence and Machine Learning'),
        ('DS', 'CSE Data Science'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
    ]
    
    username = models.CharField(max_length=150, unique=True, blank=True, null=True) # just to override the requirement
    moodleID = models.IntegerField(unique=True, primary_key=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True)
    year = models.CharField(max_length=2, choices=YEAR_CHOICES, default="FE")
    branch = models.CharField(max_length=6, choices=BRANCH_CHOICES, default="COMPS")
    is_prohibited = models.BooleanField(default=False)
    is_managing = models.BooleanField(default=False)
    USERNAME_FIELD = 'moodleID'
    REQUIRED_FIELDS = ['email']
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    objects = StudentManager()

    def __str__(self):
        return f"{self.username} ({self.moodleID})"
    
    def save(self, *args, **kwargs):
        # Auto-generate username if not provided
        if not self.username:
            self.username = f"student_{self.moodleID}"
        super().save(*args, **kwargs)