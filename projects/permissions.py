from django.http.response import Http404
from projects.models import Contributor, Project
from rest_framework import permissions


def get_project(request):
    try:
        project_id = request.parser_context["kwargs"]["project_id"]
    except KeyError:
        project_id = request.parser_context["kwargs"]["pk"]
    
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise Http404

    return project


def is_project_contributor(request):
    contributors = [user.user for user in Contributor.objects.filter(project=get_project(request))]
    return request.user in contributors


class IsOwnerOrContributor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return is_project_contributor(request)

        return get_project(request).author_user_id == request.user


class IsObjectOwnerOrContributor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return is_project_contributor(request)

        return obj.author_user_id == request.user


class IsContributor(permissions.BasePermission):

    def has_permission(self, request, view):
        return is_project_contributor(request)