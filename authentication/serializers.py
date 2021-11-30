from rest_framework import serializers
from authentication.nested_serializers.nested import SimplifiedListUserSerializer, SimplifiedDetailUserSerializer
from softdesk.nested_serializers.nested import SimplifiedListProjectsSerializer, SimplifiedContributorsSerializer, SimplifiedIssuesSerializer, SimplifiedCommentsSerializer

class UserListSerializer(SimplifiedListUserSerializer):
    pass


class UserDetailSerializer(SimplifiedDetailUserSerializer):
    projects_instances = SimplifiedListProjectsSerializer(
        many=True, read_only=True)
    contributors_instances = SimplifiedContributorsSerializer(
        many=True, read_only=True)
    issues_instances = SimplifiedIssuesSerializer(
        many=True, read_only=True)
    comments_instances = SimplifiedCommentsSerializer(
        many=True, read_only=True)
    date_joined = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    