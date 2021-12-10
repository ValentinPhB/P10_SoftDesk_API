from rest_framework import serializers

from authentication.nested_serializers.nested import SimplifiedListUserSerializer
from softdesk.nested_serializers.nested import (SimplifiedListProjectsSerializer, SimplifiedDetailProjectsSerializer,
                                                SimplifiedListContributorsSerializer,
                                                SimplifiedListIssuesSerializer, SimplifiedDetailIssuesSerializer,
                                                SimplifiedListCommentsSerializer, SimplifiedDetailCommentsSerializer)


# Projects
class ProjectsListSerializer(SimplifiedListProjectsSerializer):
    author_instance = SimplifiedListUserSerializer(read_only=True)


class ProjectsDetailSerializer(SimplifiedDetailProjectsSerializer):
    author_instance = SimplifiedListUserSerializer(read_only=True)
    contributors = SimplifiedListContributorsSerializer(
        many=True, read_only=True)
    issues = SimplifiedListIssuesSerializer(
        many=True, read_only=True)


# Contributors
class ContributorsListSerializer(SimplifiedListContributorsSerializer):
    user_instance = SimplifiedListUserSerializer(read_only=True)
    project_instance = SimplifiedListProjectsSerializer(read_only=True)


class ContributorsDetailSerializer(SimplifiedListContributorsSerializer):
    project_instance = SimplifiedListProjectsSerializer(read_only=True)


# Issues
class IssuesListSerializer(SimplifiedListIssuesSerializer):
    created_time = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)


class IssuesDetailSerializer(SimplifiedDetailIssuesSerializer):
    author_instance = SimplifiedListUserSerializer(read_only=True)
    parent_project = SimplifiedListProjectsSerializer(read_only=True)
    comments = SimplifiedListCommentsSerializer(
        many=True, read_only=True)
    created_time = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)


# Comments
class CommentsListSerializer(SimplifiedListCommentsSerializer):
    author_instance = SimplifiedListUserSerializer(read_only=True)


class CommentsDetailSerializer(SimplifiedDetailCommentsSerializer):
    author_instance = SimplifiedListUserSerializer(read_only=True)
    parent_issue = SimplifiedDetailIssuesSerializer(read_only=True)
    created_time = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
