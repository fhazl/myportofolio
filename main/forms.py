from django.forms import ModelForm, TextInput, Textarea, URLInput, DateInput
from .models import Project, Experience, Education

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