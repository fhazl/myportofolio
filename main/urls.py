from django.urls import path
from main.views import (
    show_main,
    show_projects, create_project, update_project, delete_project, get_projects_json, toggle_star_project, create_project_ajax,
    show_experience, create_experience, update_experience, delete_experience, get_experience_json, toggle_star_experience, create_experience_ajax,
        show_education, create_education, update_education, delete_education, get_education_json, toggle_star_education, create_education_ajax,
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