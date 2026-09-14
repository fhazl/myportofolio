# main/admin.py
from django.contrib import admin
from main.models import Education, Experience

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'started_at', 'is_ongoing', 'thumbnail', 'description')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'degree', 'field_of_study', 'started_at', 'is_ongoing', 'thumbnail', 'description')
