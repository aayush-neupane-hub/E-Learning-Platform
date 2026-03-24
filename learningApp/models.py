from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Model for course levels, using Django's TextChoices for better readability and maintainability
class Level(models.TextChoices):
    BEGININER = 'Beginner', 'beginner'
    INTERMEDIATE = 'Intermediate', 'intermediate'
    ADVANCED = 'Advanced', 'advanced'



# Model for user profile, extending the built-in User model with additional fields
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    



# Model for Categories, with a name field with slug field for URL-friendly representation and timestamps
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




# Model for courses, with fields for title, slug, description, thumbnail, instructor, category, publication status, level, and timestamps
class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    is_published = models.BooleanField(default=False)
    level = models.ForeignKey('Level', on_delete=models.PROTECT, related_name='courses')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

# Model for user or student review/rating
class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'





# Model for user Enrollment in the courses
class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'



# Model for Module(chapter/units) for course
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    chapter = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


# Model for Lesson for each module
class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField()
    is_published = models.BooleanField(default=False)  # To indicate if the lesson is published or not
    created_at = models.DateTimeField(auto_now_add=True)


# Model for Resource for each lesson, which can be a file or a link
class Resource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete = models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='lesson_resources/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



# Model for tracking user progress in a course, with fields for course, user, completed lessons, and timestamps
class Progress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=False)
    complete_lessons = models.ManyToManyField(Lesson, blank=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.course.title} - {"Completed" if self.is_completed else "In Progress"}'
    
