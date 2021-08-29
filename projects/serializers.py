from rest_framework import serializers
from projects.models import Project, Issue


class ProjectSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ['url', 'id', 'title', 'description', 'type', 'author']

    def create(self, validated_data):
        project = Project(**validated_data)
        project.author = self.context['request'].user
        project.save()
        return project

class IssueSerializer(serializers.HyperlinkedModelSerializer):

    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.order_by('-id'))
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        fields = ['url', 'id', 'project', 'title', 'description', 'priority', 'types', 'status', 'author']

    def create(self, validated_data):
        issue = Issue(**validated_data)
        issue.author = self.context['request'].user
        issue.save()
        return issue