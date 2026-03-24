from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/', views.lesson_view, name='lesson_view'),
    path('exams/<int:exam_id>/', views.exam, name='exam'),
    path('exams/<int:exam_id>/result/', views.exam_result, name='exam_result'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/instructor/', views.instructor_dashboard, name='instructor_dashboard'),
]
