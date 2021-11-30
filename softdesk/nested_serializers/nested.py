from rest_framework import serializers
from softdesk.models import Contributors, Projects, Issues, Comments


class SimplifiedListProjectsSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Projects
        nameservers = serializers.HyperlinkedIdentityField(
            view_name='projects-list',
            lookup_url_kwarg='projects_pk'
        )
        fields = ['id', 'type_project', 'title',
                  'description', 'url', ]


class SimplifiedDetailProjectsSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description',
                  'type_project', 'contributors', 'issues', 'author_instance']


class SimplifiedContributorsSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['id', 'user_instance',
                  'project_instance', 'permission', 'role']


class SimplifiedIssuesSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = ['id', 'author_instance', 'parent_project', 'title',
                  'description', 'created_time', 'tag', 'priority', 'status', 'comments']


class SimplifiedCommentsSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'author_instance', 'parent_issue',
                  'description', 'created_time']
