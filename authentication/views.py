from django.contrib.auth.hashers import make_password

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from authentication.permissions import IsAdminUser
from authentication.serializers import UserListSerializer, UserDetailSerializer
from authentication.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action in ['retrieve', 'update', 'create', 'delete']:
            return UserDetailSerializer
        return UserListSerializer

    # @property
    # def default_response_headers(self):
    #     headers = viewsets.ModelViewSet.default_response_headers.fget(self)
    #     headers['Authorization'] = request.auth
    #     return headers
