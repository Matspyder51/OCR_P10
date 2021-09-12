from rest_framework import permissions


class IsOwnerOrContributor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.author == request.user #or (obj.project is not None and (obj.project.author == request.user))