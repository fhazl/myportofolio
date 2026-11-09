from django.urls import path
from main.views import (
    show_main,
    show_projects,
    show_experience,
    show_education,
    register, login_user, logout_user
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    # Page Paths (data and writes go through /api/v1/)
    path("projects/", show_projects, name="show_projects"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education"),

    # Authentication Paths
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]