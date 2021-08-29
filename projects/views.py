from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.serializers import Serializer
from projects import serializers
from projects.serializers import IssueSerializer, ProjectSerializer
from projects.models import Project, Issue


# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.order_by('-id')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.order_by('-id')
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]