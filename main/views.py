from django.shortcuts import redirect, render
from django import forms
from main.models import Education, Experience

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