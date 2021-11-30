from rest_framework import serializers
from authentication.models import User


class SimplifiedListUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        nameservers = serializers.HyperlinkedIdentityField(
            view_name='user-list-detail',
            lookup_url_kwarg='user_pk'
        )
        fields = ('id', 'first_name', 'last_name',
                  'email', 'is_staff', 'is_superuser', 'url')


class SimplifiedDetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser',
                  'date_joined', 'projects_instances', 'contributors_instances',
                  'issues_instances','comments_instances', 'password')
