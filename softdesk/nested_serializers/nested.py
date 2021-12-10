from rest_framework import serializers

from softdesk.models import Contributors, Projects, Issues, Comments


# Projects
class SimplifiedListProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'type_project', 'title',  'description',
                  'author_instance', ]


class SimplifiedDetailProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'type_project', 'title', 'description',
                  'contributors', 'issues', 'author_instance', ]


# Contributors
class SimplifiedListContributorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['id', 'user_instance', 'permission',
                  'role', 'project_instance', ]


# Issues
class SimplifiedListIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = ['id', 'title', 'description',
                  'created_time', 'tag', 'priority', 'status', ]


class SimplifiedDetailIssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issues
        fields = ['id', 'author_instance', 'parent_project', 'title',
                  'description', 'created_time', 'tag', 'priority', 'status', 'comments']


# Comments
class SimplifiedListCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'author_instance', 'description', ]


class SimplifiedDetailCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'author_instance', 'parent_issue',
                  'description', 'created_time']
