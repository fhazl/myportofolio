from django.forms import ModelForm, TextInput, Textarea, URLInput, DateInput
from .models import Project, Experience, Education
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Project Name",
            "description": "Project Description",
            "tech_stack": "Technologies Used",
            "project_url": "Project URL",
            "project_image_url": "Project Image URL",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Website Portofolio",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe your project here..",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Project name cannot consist only of HTML tags.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "category",
            "title",
            "description",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "category": "Experience Category",
            "title": "Job Title",
            "description": "Job Description",
            "thumbnail": "Thumbnail Image URL",
            "started_at": "Start Date",
            "ended_at": "End Date",
        }

        widgets = {
            "category": TextInput(
                attrs={
                    "placeholder": "Full-time, Internship, Freelance",
                    "maxlength": 100,
                }
            ),
            "title": TextInput(
                attrs={
                    "placeholder": "Backend Developer",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe your responsibilities and achievements here..",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "started_at": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                }
            ),
            "ended_at": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                }
            ),
        }

    def clean_category(self):
        category = strip_tags(self.cleaned_data["category"]).strip()
        if not category:
            raise ValidationError("Category cannot consist only of HTML tags.")
        return category

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Job title cannot consist only of HTML tags.")
        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Job description cannot consist only of HTML tags.")
        return description

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "degree",
            "institution",
            "field_of_study",
            "description",
            "started_at",
            "ended_at",
        ]

        labels = {
            "degree": "Degree / Certification",
            "institution": "School or Institution",
            "field_of_study": "Field of Study",
            "description": "Education Description",
            "started_at": "Start Date",
            "ended_at": "End Date",
        }

        widgets = {
            "degree": TextInput(
                attrs={
                    "placeholder": "Bachelor's Degree",
                    "maxlength": 255,
                }
            ),
            "institution": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "field_of_study": TextInput(
                attrs={
                    "placeholder": "Computer Science",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe your academic focus or activities here..",
                    "rows": 3,
                }
            ),
            "started_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }
    def clean_degree(self):
        degree = strip_tags(self.cleaned_data["degree"]).strip()
        if not degree:
            raise ValidationError("Degree cannot consist only of HTML tags.")
        return degree

    def clean_institution(self):
        institution = strip_tags(self.cleaned_data["institution"]).strip()
        if not institution:
            raise ValidationError("Institution cannot consist only of HTML tags.")
        return institution

    def clean_field_of_study(self):
        field_of_study = strip_tags(self.cleaned_data["field_of_study"]).strip()
        if not field_of_study:
            raise ValidationError("Field of study cannot consist only of HTML tags.")
        return field_of_study

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()