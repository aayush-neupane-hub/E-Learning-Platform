from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Model for user profile, extending the built-in User model with additional fields
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    


# Model for course levels, using Django's TextChoices for better readability and maintainability
class Level(models.TextChoices):
    BEGININER = 'Beginner', 'beginner'
    INTERMEDIATE = 'Intermediate', 'intermediate'
    ADVANCED = 'Advanced', 'advanced'



# Model for courses, with fields for title, slug, description, thumbnail, instructor, category, publication status, level, and timestamps
class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='courses')
    category = models.CharField(max_length=100, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    level = models.ForeignKey('Level', on_delete=models.PROTECT, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title