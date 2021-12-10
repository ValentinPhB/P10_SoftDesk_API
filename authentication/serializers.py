from rest_framework import serializers

from authentication.nested_serializers.nested import SimplifiedListUserSerializer, SimplifiedDetailUserSerializer
from softdesk.nested_serializers.nested import (SimplifiedListProjectsSerializer, SimplifiedListContributorsSerializer,
                                                SimplifiedListIssuesSerializer, SimplifiedListCommentsSerializer)


class UserListSerializer(SimplifiedListUserSerializer):
    pass


class UserDetailSerializer(SimplifiedDetailUserSerializer):
    projects_instances = SimplifiedListProjectsSerializer(
        many=True, read_only=True)
    contributors_instances = SimplifiedListContributorsSerializer(
        many=True, read_only=True)
    issues_instances = SimplifiedListIssuesSerializer(
        many=True, read_only=True)
    comments_instances = SimplifiedListCommentsSerializer(
        many=True, read_only=True)
    date_joined = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
