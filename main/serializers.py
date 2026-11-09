from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project, Experience, Education


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "project_url", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, v):
            return _clean_required(v, "Title")

    def validate_description(self, v):
        return strip_tags(v).strip()

    def validate_tech_stack(self, v):
        return _clean_required(v, "Technologies")

class StarFieldsMixin(serializers.Serializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return any(u.pk == request.user.pk for u in obj.starred_by.all())

    def get_starred_by_names(self, obj):
        return ", ".join(u.username for u in obj.starred_by.all())

    def validate(self, attrs):
        started = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        if started and ended and ended < started:
            raise serializers.ValidationError(
                {"ended_at": "End date cannot be before start date."}
            )
        return attrs


def _clean_required(value, label):
    value = strip_tags(value).strip()
    if not value:
        raise serializers.ValidationError(f"{label} cannot be empty.")
    return value


class ExperienceSerializer(StarFieldsMixin, serializers.ModelSerializer):
    is_ongoing = serializers.BooleanField(read_only=True)

    class Meta:
        model = Experience
        fields = [
            "id", "category", "title", "description", "thumbnail",
            "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_category(self, v):
        return _clean_required(v, "Category")

    def validate_title(self, v):
        return _clean_required(v, "Title")

    def validate_description(self, v):
        return strip_tags(v).strip()


class EducationSerializer(StarFieldsMixin, serializers.ModelSerializer):
    is_ongoing = serializers.BooleanField(read_only=True)

    class Meta:
        model = Education
        fields = [
            "id", "degree", "institution", "field_of_study", "description",
            "thumbnail", "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_degree(self, v):
        return _clean_required(v, "Degree")

    def validate_institution(self, v):
        return _clean_required(v, "Institution")

    def validate_field_of_study(self, v):
        return _clean_required(v, "Field of study")

    def validate_description(self, v):
        return strip_tags(v).strip()