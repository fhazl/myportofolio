from django.shortcuts import render

from main.models import Experience


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