from itertools import chain

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from authentication.models import User
from softdesk.models import Contributors, Projects, Issues, Comments
from softdesk.serializers import (ContributorsListSerializer, ContributorsDetailSerializer, ProjectsListSerializer,
                                  ProjectsDetailSerializer, IssuesListSerializer, IssuesDetailSerializer,
                                  CommentsListSerializer, CommentsDetailSerializer)
from softdesk.permissions import ProjectRights, ContributorsRights, IssuesRights, CommentsRights


class ContributorsViewSet(ModelViewSet):
    queryset = Contributors.objects.all()
    serializer_class = ContributorsListSerializer
    detail_serializer_class = ContributorsListSerializer
    permission_classes = (IsAuthenticated, ContributorsRights,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contributor_instance = self.perform_create(serializer, request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, request):
        user_instance = User.objects.get(pk=request.data['user_instance'])
        project_instance = Projects.objects.get(pk=self.kwargs['projects_pk'])
        try:
            Contributors.objects.get(
                user_instance=user_instance, project_instance=project_instance)
            raise serializers.ValidationError(
                'ATTENTION; Cet utilisateur est déja associé à ce projet.')
        except ObjectDoesNotExist:
            contributor = serializer.save(project_instance=project_instance)

    def get_queryset(self):
        return super().get_queryset().filter(project_instance=self.kwargs['projects_pk'])

    def get_object(self):
        obj = get_object_or_404(Contributors, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        if self.action == 'list':
            return ContributorsListSerializer
        if self.action in ['retrieve', 'create', 'update', 'delete']:
            return ContributorsDetailSerializer
        return ContributorsListSerializer


class ProjectsViewSet(ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsListSerializer
    detail_serializer_class = ProjectsDetailSerializer
    permission_classes = (IsAuthenticated, ProjectRights,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        project = serializer.save(author_instance=self.request.user)
        project_complete = Projects.objects.get(id=project.id)

        # Create a contributor instance with author and add it to the project.
        author_contributor = Contributors.objects.create(
            user_instance=self.request.user, project_instance=project, role="AUTEUR", permission="AUTEUR")
        project_complete.contributors.add(author_contributor)

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return super().get_queryset()
        author = super().get_queryset().filter(author_instance=self.request.user.id)
        contributor = [Projects.objects.get(
            pk=_.project_instance.id) for _ in Contributors.objects.filter(user_instance=self.request.user.id)]
        return list(set(chain(author, contributor)))

    def get_object(self):
        obj = get_object_or_404(Projects, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectsListSerializer
        if self.action in ['retrieve', 'update', 'delete']:
            return ProjectsDetailSerializer
        return ProjectsListSerializer


class IssuesViewSet(ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesListSerializer
    detail_serializer_class = IssuesDetailSerializer
    permission_classes = (IsAuthenticated, IssuesRights,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        issues_instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        parent_project = Projects.objects.get(pk=self.kwargs['projects_pk'])
        issue = serializer.save(
            author_instance=self.request.user, parent_project=parent_project)

    def get_queryset(self):
        return super().get_queryset().filter(parent_project=self.kwargs['projects_pk'])

    def get_object(self):
        obj = get_object_or_404(Issues, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        if self.action == 'list':
            return IssuesListSerializer
        if self.action in ['retrieve', 'update', 'delete']:
            return IssuesDetailSerializer
        return IssuesListSerializer


class CommentsViewSet(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsListSerializer
    detail_serializer_class = CommentsDetailSerializer
    permission_classes = (IsAuthenticated, CommentsRights,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment_instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        parent_issue = Issues.objects.get(pk=self.kwargs['issues_pk'])
        issue = serializer.save(
            author_instance=self.request.user, parent_issue=parent_issue)

    def get_queryset(self):
        return super().get_queryset().filter(parent_issue=self.kwargs['issues_pk'])

    def get_object(self):
        obj = get_object_or_404(Comments, pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentsListSerializer
        if self.action in ['retrieve', 'update', 'delete']:
            return CommentsDetailSerializer
        return CommentsListSerializer
