from django.urls import path

from main.views import (
    show_main,
    show_experience,
    add_experience,
    show_education,
    add_education,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", add_experience, name="add_experience"),
    path("education/", show_education, name="show_education"),
    path("education/add/", add_education, name="add_education"),
]