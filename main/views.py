from django.shortcuts import redirect, render
from main.models import Education, Experience, Project
from main.forms import ProjectForm, ExperienceForm, EducationForm

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime
from django.views.decorators.http import ensure_csrf_cookie

# ==========================================
# AUTHENTICATION VIEWS
# ==========================================

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")

    context = {
        "name": "Fernando Hazel",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Fernando Hazel",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# ==========================================
# PAGE VIEWS (static shells; data comes from /api/v1/)
# ==========================================

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No active login session / Cookie not found')
    context = {
        "name": "Fernando Hazel",
        "npm": "2506587195",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan keamanan siber."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)

@ensure_csrf_cookie
def show_projects(request):
    return render(request, "project.html", {"name": "Fernando Hazel"})

@ensure_csrf_cookie
def show_experience(request):
    return render(request, "experience.html", {"name": "Fernando Hazel"})

@ensure_csrf_cookie
def show_education(request):
    return render(request, "education.html", {"name": "Fernando Hazel"})