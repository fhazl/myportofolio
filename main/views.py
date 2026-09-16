from django.shortcuts import redirect, render
from django import forms
from main.models import Education, Experience, Project
from main.forms import ProjectForm

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Burhan",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['category', 'title', 'description', 'thumbnail', 'started_at', 'ended_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'started_at': forms.DateInput(attrs={'type': 'date'}),
            'ended_at': forms.DateInput(attrs={'type': 'date'}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'field_of_study', 'description', 'started_at', 'ended_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'started_at': forms.DateInput(attrs={'type': 'date'}),
            'ended_at': forms.DateInput(attrs={'type': 'date'}),
        }

def show_main(request):
    context = {
        "name": "Fernando Hazel",
        "npm": "2506587195",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "A Computer Science student at Universitas Indonesia interested "
            "in software development and cybersecurity."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Fernando Hazel",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def add_experience(request):
    form = ExperienceForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("main:show_experience")
    context = {
        "name": "Fernando Hazel",
        "form": form
    }
    return render(request, "add_experience.html", context)

def show_education(request):
    context = {
        "name": "Fernando Hazel",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)


def add_education(request):
    form = EducationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("main:show_education")
    context = {
        "name": "Fernando Hazel",
        "form": form
    }
    return render(request, "add_education.html", context)