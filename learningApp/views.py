from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import Profile


SAMPLE_COURSES = [
    {
        "id": 1,
        "title": "Python for Absolute Beginners",
        "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=900&q=80",
        "rating": 4.7,
        "progress": 72,
        "description": "Build real-world Python projects with clear step-by-step guidance.",
    },
    {
        "id": 2,
        "title": "Modern Web Development",
        "image": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80",
        "rating": 4.5,
        "progress": 48,
        "description": "Learn frontend and backend fundamentals for professional web apps.",
    },
    {
        "id": 3,
        "title": "Data Analysis with SQL",
        "image": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=900&q=80",
        "rating": 4.8,
        "progress": 85,
        "description": "Master SQL queries and analytical thinking for data-driven decisions.",
    },
]


def get_or_create_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user, defaults={"role": "Student"})
    return profile


def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url="login")
        def _wrapped_view(request, *args, **kwargs):
            profile = get_or_create_profile(request.user)
            if profile.role != required_role:
                messages.error(request, f"You are not authorized to access the {required_role.lower()} area.")
                if profile.role == "Instructor":
                    return redirect("instructor_dashboard")
                return redirect("student_dashboard")
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator



def home(request):
    context = {"featured_courses": SAMPLE_COURSES}
    return render(request, "pages/home.html", context)


def login_view(request):
    if request.user.is_authenticated:
        profile = get_or_create_profile(request.user)
        if profile.role == "Instructor":
            return redirect("instructor_dashboard")
        return redirect("student_dashboard")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            messages.error(request, "Invalid email or password.")
            return render(request, "pages/accounts/login.html")

        authenticated_user = authenticate(request, username=user.username, password=password)
        if not authenticated_user:
            messages.error(request, "Invalid email or password.")
            return render(request, "pages/accounts/login.html")

        login(request, authenticated_user)
        profile = get_or_create_profile(authenticated_user)

        if profile.role == "Instructor":
            return redirect("instructor_dashboard")
        return redirect("student_dashboard")

    return render(request, "pages/accounts/login.html")


def signup_view(request):
    if request.user.is_authenticated:
        profile = get_or_create_profile(request.user)
        if profile.role == "Instructor":
            return redirect("instructor_dashboard")
        return redirect("student_dashboard")

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        role = request.POST.get("role", "Student")

        if role not in ["Student", "Instructor"]:
            role = "Student"

        if not full_name or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, "pages/accounts/signup.html")

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, "pages/accounts/signup.html")

        base_username = email.split("@")[0] or "user"
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name,
        )
        Profile.objects.create(user=user, role=role)
        login(request, user)

        if role == "Instructor":
            return redirect("instructor_dashboard")
        return redirect("student_dashboard")

    return render(request, "pages/accounts/signup.html")


@login_required(login_url="login")
def profile(request):
    return render(request, "pages/accounts/profile.html")


def course_list(request):
    context = {"courses": SAMPLE_COURSES}
    return render(request, "pages/courses/course_list.html", context)


def course_detail(request, course_id):
    course = next((course for course in SAMPLE_COURSES if course["id"] == course_id), SAMPLE_COURSES[0])
    lessons = [
        {"id": 1, "title": "Introduction", "duration": "08:12"},
        {"id": 2, "title": "Core Concepts", "duration": "14:48"},
        {"id": 3, "title": "Hands-on Practice", "duration": "18:05"},
    ]
    context = {"course": course, "lessons": lessons}
    return render(request, "pages/courses/course_detail.html", context)


def lesson_view(request, course_id, lesson_id):
    lesson = {
        "id": lesson_id,
        "title": f"Lesson {lesson_id}",
        "content": "This lesson covers practical concepts with guided examples and implementation details.",
    }
    context = {"course_id": course_id, "lesson": lesson}
    return render(request, "pages/courses/lesson_view.html", context)


def exam(request, exam_id):
    questions = [
        {"id": 1, "text": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "High Text Machine Language", "Home Tool Markup Language", "Hyperlinks and Text Markup Language"]},
        {"id": 2, "text": "Which CSS property controls text color?", "options": ["font-style", "text-color", "color", "foreground"]},
    ]
    context = {"exam_id": exam_id, "questions": questions}
    return render(request, "pages/exams/exam.html", context)


def exam_result(request, exam_id):
    context = {
        "exam_id": exam_id,
        "score": 88,
        "correct_answers": 22,
        "total_questions": 25,
    }
    return render(request, "pages/exams/result.html", context)


@role_required("Student")
def student_dashboard(request):
    context = {"courses": SAMPLE_COURSES}
    return render(request, "pages/dashboard/student_dashboard.html", context)


@role_required("Instructor")
def instructor_dashboard(request):
    context = {"courses": SAMPLE_COURSES}
    return render(request, "pages/dashboard/instructor_dashboard.html", context)


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")