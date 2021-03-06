from django.contrib.auth.hashers import make_password

from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from authentication.permissions import IsAdminUser
from authentication.serializers import UserListSerializer, UserDetailSerializer, UserDetailAdminSerializer
from authentication.models import User


class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()
            
    def get_serializer_class(self):
        if self.request.user.is_anonymous:
            return UserDetailSerializer
        elif self.request.user.is_superuser or self.request.user.is_staff:
            return UserDetailAdminSerializer
        return UserDetailSerializer


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

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action in ['retrieve', 'update', 'create', 'delete']:
            return UserDetailSerializer
        return UserListSerializer
