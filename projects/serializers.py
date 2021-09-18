from rest_framework import serializers
from projects.models import Contributor, Project, Issue, IssueComment


class ProjectSerializer(serializers.ModelSerializer):
    author_user_id = serializers.ReadOnlyField(source='author_user_id.id')

    class Meta:
        model = Project
        fields = '__all__'


class ProjectListSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author_user_id.username')

    class Meta:
        model = Project
        fields = ['id', 'title', 'author_user_id', 'author_username']


class IssueSerializer(serializers.ModelSerializer):
    author_user_id = serializers.ReadOnlyField(source='author_user_id.id')
    project_id = serializers.ReadOnlyField(source='project_id.id')

    class Meta:
        model = Issue
        fields = '__all__'


class IssueListSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(
        source='author_user_id.username'
    )
    assignee_username = serializers.ReadOnlyField(
        source='assignee_user_id.username'
    )

    class Meta:
        model = Issue
        fields = [
            'id',
            'author_username',
            'title',
            'description',
            'types',
            'priority',
            'status',
            'created_time',
            'assignee_username',
        ]


class IssueCommentSerializer(serializers.ModelSerializer):
    author_user_id = serializers.ReadOnlyField(source='author_user_id.id')
    issue_id = serializers.ReadOnlyField(source='issue.id')

    class Meta:

        model = IssueComment
        fields = '__all__'


class IssueCommentListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IssueComment
        fields = ['id', 'description']

class ContributorSerializer(serializers.ModelSerializer):
    project_id = serializers.ReadOnlyField(source="project.id")

    class Meta:
        model = Contributor
        fields = "__all__"

class ContributorListSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = Contributor
        fields = ['user_id', 'username']