from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

# Model for course levels, using Django's TextChoices for better readability and maintainability
class Level(models.TextChoices):
    BEGINNER = 'Beginner', 'beginner'
    INTERMEDIATE = 'Intermediate', 'intermediate'
    ADVANCED = 'Advanced', 'advanced'



# Model for user profile, extending the built-in User model with additional fields
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = RichTextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=[('Student', 'Student'), ('Instructor', 'Instructor')], default='Student')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    



# Model for Categories, with tree hierarchy support via django-mptt
class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.PROTECT, related_name='children', blank=True, null=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name




# Model for courses, with fields for title, slug, description, thumbnail, instructor, category, publication status, level, and timestamps
class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = RichTextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    is_published = models.BooleanField(default=False)
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.BEGINNER)
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
    description = RichTextField(blank=True, null=True)
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


# Model for Lesson for each module
class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True, null=True)
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
    


# Model for Quiz, with fields for course, title, time limit, total marks, publication status, and timestamps
class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    time_limit = models.PositiveIntegerField(help_text='Time limit in minutes')
    total_marks = models.PositiveIntegerField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



# Model for Question, with fields for quiz, text, and marks
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = RichTextField()
    marks = models.PositiveIntegerField()


# Model for Option, with fields for question, text, and whether it's the correct answer or not
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = RichTextField()
    is_correct = models.BooleanField(default=False)


# Model for tracking quiz attempts by users, with fields for quiz, user, and timestamp of the attempt
class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='quiz_attempts')
    attempted_at = models.DateTimeField(auto_now_add=True)



class Submission(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='submissions')
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    feedback = RichTextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)



class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)



# Model for progress tracking and Analytics
class CourseProgress(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='course_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_progress')
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    completed_lessons = models.ManyToManyField(Lesson, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)



# Model for Comment / discussion on courses or lessons
class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    context = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)



# model for notifications to users about course updates, new courses, or other relevant information
class Notification(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
    message = RichTextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



# Model for Wishlist, allowing users to save courses they are interested in for future reference
class Wishlist(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='wishlist')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_at = models.DateTimeField(auto_now_add=True)



# MOdel for Certification, allowing users to earn certificates upon course completion
class Certificate(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    certificate_id = models.CharField(max_length=255, unique=True)
    certificate_file = models.FileField(upload_to='certificates/' , blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# Model for Payment, allowing users to make payments for courses they want to enroll in
class Payment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='payments', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')
    transaction_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)



# Model for Instructor / Caurse Analytics, allowing instructors to track the performance of their courses and students
class CourseAnalytics(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='analytics')
    total_enrollments = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)