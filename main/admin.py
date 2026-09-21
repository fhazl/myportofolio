from django.contrib import admin
from main.models import Project, Experience, Education

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'tech_stack', 'project_url', 'project_image_url')
    search_fields = ('title', 'tech_stack')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'started_at', 'get_status', 'thumbnail') # Added 'category' back!
    search_fields = ('title', 'description', 'category')

    @admin.display(description="End Date / Status")
    def get_status(self, obj):
        return obj.ended_at if obj.ended_at else "Present"

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'degree', 'field_of_study', 'started_at', 'get_status')
    search_fields = ('institution', 'degree', 'field_of_study')

    @admin.display(description="End Date / Status")
    def get_status(self, obj):
        return obj.ended_at if obj.ended_at else "Present"