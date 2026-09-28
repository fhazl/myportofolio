from django.shortcuts import redirect, render, get_object_or_404
from main.models import Education, Experience, Project
from main.forms import ProjectForm, ExperienceForm, EducationForm

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotAllowed

from main.permissions import owner_required, editor_or_owner_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime
from django.contrib.auth.decorators import login_required

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
# MAIN VIEW
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


# ==========================================
# PROJECT VIEWS
# ==========================================

@owner_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Project Successfully Added!")
        return redirect("main:show_projects")

    context = {"name": "Fernando Hazel", "form": form, "is_update": False}
    return render(request, "projects_form.html", context)

@editor_or_owner_required
def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project successfully updated!")
        return redirect("main:show_projects")

    context = {"name": "Fernando Hazel", "form": form, "is_update": True}
    return render(request, "projects_form.html", context)

def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)

    context = {
        "name": "Fernando Hazel",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

@owner_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project successfully deleted!")
    return redirect("main:show_projects")

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)
    
    projects_json = serializers.serialize(
        "json", 
        projects, 
        fields=('id', 'title', 'description', 'tech_stack', 'project_url', 'project_image_url')
    )
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="/login/")
def toggle_star_project(request, project_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    project = get_object_or_404(Project, pk=project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    return redirect("main:show_projects")


# ==========================================
# EXPERIENCE VIEWS
# ==========================================

@owner_required
def create_experience(request):
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience successfully added!")
        return redirect("main:show_experience")

    context = {"name": "Fernando Hazel", "form": form, "is_update": False}
    return render(request, "experience_form.html", context)

@editor_or_owner_required
def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience successfully updated!")
        return redirect("main:show_experience")

    context = {"name": "Fernando Hazel", "form": form, "is_update": True}
    return render(request, "experience_form.html", context)

def show_experience(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    context = {
        "name": "Fernando Hazel",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)

@owner_required
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience successfully deleted!")
    return redirect("main:show_experience")

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)
        
    experiences_json = serializers.serialize(
        "json", 
        experiences, 
        fields=('id', 'category', 'title', 'description', 'thumbnail', 'started_at', 'ended_at')
    )
    return HttpResponse(experiences_json, content_type="application/json")

@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    experience = get_object_or_404(Experience, pk=experience_id)
    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)
    return redirect("main:show_experience")


# ==========================================
# EDUCATION VIEWS
# ==========================================

@owner_required
def create_education(request):
    form = EducationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New education successfully added!")
        return redirect("main:show_education")

    context = {"name": "Fernando Hazel", "form": form, "is_update": False}
    return render(request, "education_form.html", context)

@editor_or_owner_required
def update_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education successfully updated!")
        return redirect("main:show_education")

    context = {"name": "Fernando Hazel", "form": form, "is_update": True}
    return render(request, "education_form.html", context)

def show_education(request):
    degree_query = request.GET.get("degree", "").strip()
    educations = Education.objects.all()
    if degree_query:
        educations = educations.filter(degree__icontains=degree_query)

    context = {
        "name": "Fernando Hazel",
        "education_list": educations,
        "degree_query": degree_query,
    }
    return render(request, "education.html", context)

@owner_required
def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    if request.method == "POST":
        education.delete()
        messages.success(request, "Education successfully deleted!")
    return redirect("main:show_education")

def get_education_json(request):
    degree_query = request.GET.get("degree", "").strip()
    educations = Education.objects.all()
    if degree_query:
        educations = educations.filter(degree__icontains=degree_query)
        
    educations_json = serializers.serialize(
        "json", 
        educations, 
        fields=('id', 'degree', 'institution', 'field_of_study', 'description', 'thumbnail', 'started_at', 'ended_at')
    )
    return HttpResponse(educations_json, content_type="application/json")

@login_required(login_url="/login/")
def toggle_star_education(request, education_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    education = get_object_or_404(Education, pk=education_id)
    if education.starred_by.filter(pk=request.user.pk).exists():
        education.starred_by.remove(request.user)
    else:
        education.starred_by.add(request.user)
    return redirect("main:show_education")