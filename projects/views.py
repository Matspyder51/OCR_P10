from rest_framework.response import Response
from projects.permissions import IsOwnerOrContributor
from rest_framework import viewsets, permissions, generics
from rest_framework.serializers import Serializer
from projects import serializers
from projects.serializers import IssueSerializer, ProjectSerializer, IssueCommentListSerializer
from projects.models import Project, Issue, IssueComment, Contributor

# Create your views here.

def serializer_method(self, model):
    if self.request.method == 'GET':
        return eval('serializers.' + model + 'ListSerializer')
    return eval('serializers.' + model + 'Serializer')


def queryset_filter(self, obj):
    if obj == 'project_id':
        return self.queryset.filter(project_id=self.kwargs.get(obj))
    if obj == 'issue_id':
        return self.queryset.filter(issue=self.kwargs.get(obj))


class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return serializer_method(self, 'Project')

    def get_queryset(self):
        contributors_list = [project.project for project in Contributor.objects.filter(user=self.request.user)]
        return contributors_list

    def perform_create(self, serializer):
        project = serializer.save(author_user_id=self.request.user)
        contributor = Contributor.objects.create(
            user=self.request.user,
            project=project
        )
        contributor.save()


class ProjectDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'put', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Project deleted")


class IssueList(generics.ListCreateAPIView):
    queryset = Issue.objects.all().order_by('-id')
    serializer_class = serializers.IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return queryset_filter(self, 'project_id')

    def get_serializer_class(self):
        return serializer_method(self, 'Issue')


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all().order_by('-id')
    serializer_class = serializers.IssueSerializer
    permission_classes = [permissions.IsAuthenticated]
    # http_method_names = ['put', 'delete']

class IssueCommentList(generics.ListCreateAPIView):
    queryset = IssueComment.objects.all()
    serializer_class = serializers.IssueCommentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return queryset_filter(self, 'issue_id')

    def get_serializer_class(self):
        return serializer_method(self, 'IssueComment')

class IssueCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = IssueComment.objects.all()
    serializer_class = serializers.IssueCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    # http_method_names = ['get', 'put', 'delete']