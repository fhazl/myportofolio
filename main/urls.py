from django.urls import path

from main.views import (
    show_main,
    show_experience,
    add_experience,
    show_education,
    add_education,
    create_project,
    show_projects, 
    create_project,
    get_projects_json,
    delete_project
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/", show_projects, name="show_projects"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", add_experience, name="add_experience"),
    path("education/", show_education, name="show_education"),
    path("education/add/", add_education, name="add_education"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project")
]