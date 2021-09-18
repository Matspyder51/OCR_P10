from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from projects.permissions import IsOwnerOrContributor, IsObjectOwnerOrContributor, IsContributor
from rest_framework import viewsets, permissions, generics
from rest_framework.serializers import Serializer
from projects import serializers
from projects.serializers import IssueSerializer, ProjectSerializer, IssueCommentListSerializer
from projects.models import Project, Issue, IssueComment, Contributor


# Create your views here.
def get_contributors(self):
    return [user.user.id for user in Contributor.objects.filter(project=self.kwargs['project_id'])]

def serializer_method(self, model):
    if self.request.method == 'GET':
        return eval('serializers.' + model + 'ListSerializer')
    return eval('serializers.' + model + 'Serializer')


def queryset_filter(self, obj):
    if obj == 'project_id':
        return self.queryset.filter(project_id=self.kwargs.get(obj))
    if obj == 'issue_id':
        return self.queryset.filter(issue=self.kwargs.get(obj))

def is_user_assignee(self):
    if int(self.request.data['assignee_user_id']) not in get_contributors(self):
        raise ValidationError("The user isn't a collaborator of the project")


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
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrContributor]
    http_method_names = ['get', 'put', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Project deleted")


class IssueList(generics.ListCreateAPIView):
    queryset = Issue.objects.all().order_by('-id')
    serializer_class = serializers.IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_queryset(self):
        return queryset_filter(self, 'project_id')

    def get_serializer_class(self):
        return serializer_method(self, 'Issue')

    def perform_create(self, serializer):
        is_user_assignee(self)
        project = Project.objects.get(pk=self.kwargs['project_id'])
        serializer.save(
            author=self.request.user,
            project_id=project
        )


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all().order_by('-id')
    serializer_class = serializers.IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectOwnerOrContributor]
    http_method_names = ['get', 'put', 'delete']

    def perform_update(self, serializer):
        is_user_assignee(self)
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Issue deleted")


class IssueCommentList(generics.ListCreateAPIView):
    queryset = IssueComment.objects.all()
    serializer_class = serializers.IssueCommentListSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def get_queryset(self):
        return queryset_filter(self, 'issue_id')

    def get_serializer_class(self):
        return serializer_method(self, 'IssueComment')

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs['issue_id'])
        serializer.save(
            author=self.request.user,
            issue=issue
        )


class IssueCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = IssueComment.objects.all()
    serializer_class = serializers.IssueCommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsObjectOwnerOrContributor]
    http_method_names = ['get', 'put', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("IssueComment deleted")

class ContributorList(generics.ListCreateAPIView):
    serializer_class = serializers.ContributorSerializer
    queryset = Contributor.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrContributor]

    def get_queryset(self):
        return queryset_filter(self, 'project_id')
    
    def get_serializer_class(self):
        return serializer_method(self, 'Contributor')

    def perform_create(self, serializer):
        project_id = Project.objects.get(pk=self.kwargs['project_id'])
        if int(self.request.data["user"]) in get_contributors(self):
            raise ValidationError("This user is already contributor of this project")
        
        return serializer.save(project=project_id)

class ContributorDelete(generics.DestroyAPIView):
    serializer_class = serializers.ContributorSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrContributor
    ]

    def get_queryset(self):
        queryset = Contributor.objects.filter(pk=self.kwargs['pk'])
        return queryset

    def destroy(self, request, *args, **kwargs):
        try:
            instance = Contributor.objects.get(
                user=User.objects.get(pk=self.kwargs['pk']),
                project=Project.objects.get(pk=self.kwargs['project_id'])
            )
            user = User.objects.get(pk=self.kwargs['pk'])
            author_project = Project.objects.get(
                pk=self.kwargs['project_id']
            ).author_user_id
            if user == author_project:
                raise ValidationError("You can't delete the author of the project")
            self.perform_destroy(instance)
            return Response("User deleted")
        except User.DoesNotExist:
            raise ValidationError("This user doesn't exist")
        except Contributor.DoesNotExist:
            raise ValidationError("This user isn't contributor of this project" )