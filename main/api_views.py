from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Project, Experience, Education
from main.permissions import (
    IsPortfolioOwnerOrReadOnly, IsPortfolioOwnerOrEditorOrReadOnly,
)
from main.serializers import (
    ProjectSerializer, ExperienceSerializer, EducationSerializer,
)


def _list(request, model, serializer_class, search_param, order_by=("-started_at", "id")):
    if request.method in ("GET", "HEAD"):
        qs = model.objects.prefetch_related("starred_by")
        qs = qs.order_by(*order_by) if isinstance(order_by, (list, tuple)) else qs.order_by(order_by)
        q = request.query_params.get(search_param, "").strip()
        if q:
            qs = qs.filter(**{f"{search_param}__icontains": q})
        return Response(serializer_class(qs, many=True, context={"request": request}).data)
    serializer = serializer_class(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def _detail(request, model, serializer_class, pk):
    obj = get_object_or_404(model.objects.prefetch_related("starred_by"), pk=pk)
    if request.method in ("GET", "HEAD"):
        return Response(serializer_class(obj, context={"request": request}).data)
    if request.method == "DELETE":
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = serializer_class(
        obj, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


def _star(request, model, serializer_class, pk):
    obj = get_object_or_404(model, pk=pk)
    if obj.starred_by.filter(pk=request.user.pk).exists():
        obj.starred_by.remove(request.user)
    else:
        obj.starred_by.add(request.user)
    obj = model.objects.prefetch_related("starred_by").get(pk=pk)
    return Response(serializer_class(obj, context={"request": request}).data)


# ---------- PROJECT ----------
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    return _list(request, Project, ProjectSerializer, "title", order_by=("title", "id"))


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    return _detail(request, Project, ProjectSerializer, project_id)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    return _star(request, Project, ProjectSerializer, project_id)


# ---------- EXPERIENCE ----------
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def experience_list(request):
    return _list(request, Experience, ExperienceSerializer, "title")


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    return _detail(request, Experience, ExperienceSerializer, experience_id)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    return _star(request, Experience, ExperienceSerializer, experience_id)


# ---------- EDUCATION ----------
@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def education_list(request):
    return _list(request, Education, EducationSerializer, "degree")


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def education_detail(request, education_id):
    return _detail(request, Education, EducationSerializer, education_id)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def education_star(request, education_id):
    return _star(request, Education, EducationSerializer, education_id)