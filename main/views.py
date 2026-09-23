from django.shortcuts import redirect, render, get_object_or_404
from main.models import Education, Experience, Project
from main.forms import ProjectForm, ExperienceForm, EducationForm

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# MAIN VIEW
def show_main(request):
    last_login = request.COOKIES.get('last_login', 'No active login session / Cookie not found')
    context = {
        "name": "Burhan",
        "npm": "2206000000",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


# PROJECT VIEWS

@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Project Successfully Added!")
        return redirect("main:show_projects")

    context = {"name": "Fernando Hazel", "form": form, "is_update": False}
    return render(request, "projects_form.html", context)

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
    json_response = get_projects_json(request)
    projects = serializers.deserialize("json", json_response.content.decode("utf-8"))
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Fernando Hazel",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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
    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")

# EXPERIENCE VIEWS

def create_experience(request):
    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience successfully added!")
        return redirect("main:show_experience")

    context = {"name": "Fernando Hazel", "form": form, "is_update": False}
    return render(request, "experience_form.html", context)

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
    json_response = get_experience_json(request)
    experiences = serializers.deserialize("json", json_response.content.decode("utf-8"))
    experiences = [exp.object for exp in experiences]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Fernando Hazel",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)

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
    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

# EDUCATION VIEWS

def create_education(request):
    form = EducationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New education successfully added!")
        return redirect("main:show_education")

    context = {"name": "Fernando Hazel", "form": form, "is_update": False}
    return render(request, "education_form.html", context)

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
    json_response = get_education_json(request)
    educations = serializers.deserialize("json", json_response.content.decode("utf-8"))
    educations = [edu.object for edu in educations]
    degree_query = request.GET.get("degree", "").strip()

    context = {
        "name": "Fernando Hazel",
        "education_list": educations,
        "degree_query": degree_query,
    }
    return render(request, "education.html", context)

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
    educations_json = serializers.serialize("json", educations)
    return HttpResponse(educations_json, content_type="application/json")

# AUTHENTICATION VIEWS

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")

    context = {
        "name": "Burhan",
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
        "name": "Burhan",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # If this account has already starred it, remove the star.
        # If not, add one.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")