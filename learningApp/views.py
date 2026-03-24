from django.shortcuts import render


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



def home(request):
    context = {"featured_courses": SAMPLE_COURSES}
    return render(request, "pages/home.html", context)


def login_view(request):
    return render(request, "pages/accounts/login.html")


def signup_view(request):
    return render(request, "pages/accounts/signup.html")


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


def student_dashboard(request):
    context = {"courses": SAMPLE_COURSES}
    return render(request, "pages/dashboard/student_dashboard.html", context)


def instructor_dashboard(request):
    context = {"courses": SAMPLE_COURSES}
    return render(request, "pages/dashboard/instructor_dashboard.html", context)