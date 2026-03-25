from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin
from .models import *

# Register your models here.


def show_img(obj, field_name, width=50, height=50):
    image_field = getattr(obj, field_name, None)
    if image_field:
        return format_html('<img src="{}" width="{}" height="{}" style="object-fit:cover;border-radius:4px;" />', image_field.url, width, height)
    return "No Image"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'bio', 'show_profile_picture', 'created_at')
    search_fields = ('user__username', 'role')
    list_filter = ('role', 'created_at')

    def show_profile_picture(self, obj):
        return show_img(obj, 'profile_picture')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'level', 'price', 'is_published', 'show_thumbnail', 'created_at')
    search_fields = ('title', 'slug', 'instructor__user__username', 'category__name')
    list_filter = ('is_published', 'level', 'category', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

    def show_thumbnail(self, obj):
        return show_img(obj, 'thumbnail')

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    search_fields = ('course__title', 'user__user__username')
    list_filter = ('rating', 'created_at')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'is_active', 'enrolled_at')
    search_fields = ('course__title', 'user__user__username')
    list_filter = ('is_active', 'enrolled_at')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    search_fields = ('title', 'chapter', 'course__title')
    list_filter = ('course', 'created_at')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order', 'is_published', 'created_at')
    search_fields = ('title', 'module__title', 'module__course__title')
    list_filter = ('is_published', 'created_at')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'created_at')
    search_fields = ('title', 'lesson__title')


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'is_completed', 'completed_at')
    search_fields = ('course__title', 'user__user__username')
    list_filter = ('is_completed',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'time_limit', 'total_marks', 'is_published', 'created_at')
    search_fields = ('title', 'course__title')
    list_filter = ('is_published', 'created_at')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'marks')
    search_fields = ('quiz__title',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_correct')
    list_filter = ('is_correct',)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'attempted_at')
    search_fields = ('quiz__title', 'user__user__username')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'score', 'submitted_at')
    search_fields = ('lesson__title', 'user__user__username')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('submission', 'question', 'selected_option')


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'progress_percentage', 'last_accessed')
    search_fields = ('course__title', 'user__user__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'lesson', 'created_at')
    search_fields = ('user__user__username', 'course__title', 'lesson__title')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_read', 'created_at')
    search_fields = ('user__user__username',)
    list_filter = ('is_read', 'created_at')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'added_at')
    search_fields = ('user__user__username', 'course__title')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_id', 'user', 'course', 'created_at')
    search_fields = ('certificate_id', 'user__user__username', 'course__title')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'course', 'amount', 'payment_method', 'payment_status', 'created_at')
    search_fields = ('transaction_id', 'user__user__username', 'course__title', 'payment_method')
    list_filter = ('payment_status', 'payment_method', 'created_at')


@admin.register(CourseAnalytics)
class CourseAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('course', 'total_enrollments', 'average_rating', 'total_reviews', 'created_at')
    search_fields = ('course__title',)