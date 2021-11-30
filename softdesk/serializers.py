from authentication.nested_serializers.nested import SimplifiedListUserSerializer
from softdesk.nested_serializers.nested import SimplifiedListProjectsSerializer, SimplifiedContributorsSerializer, SimplifiedIssuesSerializer, SimplifiedCommentsSerializer
from softdesk.models import Contributors, Projects, Issues, Comments
from rest_framework import serializers


class ProjectsListSerializer(SimplifiedListProjectsSerializer):
    pass


class ProjectsDetailSerializer(SimplifiedDetailProjectsSerializer):
    author_instance = SimplifiedListUserSerializer(read_only=True)
    contributors = SimplifiedContributorsSerializer(
        many=True, queryset=Contributors.objects.all())
    issues = SimplifiedIssuesSerializer(
        many=True, queryset=Issues.objects.all())


class ContributorsListSerializer(SimplifiedContributorsSerializer):
    user_instance = SimplifiedListUserSerializer(read_only=True)
    project_instance = SimplifiedListProjectsSerializer(read_only=True)


class ContributorsDetailSerializer(SimplifiedContributorsSerializer):
    user_instance = SimplifiedListUserSerializer(read_only=True)
    project_instance = SimplifiedListProjectsSerializer(read_only=True)


class IssuesListSerializer(SimplifiedIssuesSerializer):
    author_instance = SimplifiedListUserSerializer(read_only=True)
    parent_project = SimplifiedListProjectsSerializer(read_only=True)
    comments = SimplifiedCommentsSerializer(
        many=True, queryset=Comments.objects.all())
    created_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")


class IssuesDetailSerializer(SimplifiedIssuesSerializer):
    author_instance = SimplifiedListUserSerializer(read_only=True)
    parent_project = SimplifiedListProjectsSerializer(read_only=True)
    comments = SimplifiedCommentsSerializer(
        many=True, queryset=Comments.objects.all())
    created_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")


class CommentsListSerializer(SimplifiedCommentsSerializer):
    author_instance = SimplifiedListUserSerializer(read_only=True)
    parent_issue = SimplifiedIssuesSerializer(read_only=True)
    created_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")


class CommentsDetailSerializer(SimplifiedCommentsSerializer):
    author_instance = SimplifiedListUserSerializer(read_only=True)
    parent_issue = SimplifiedIssuesSerializer(read_only=True)
    created_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
