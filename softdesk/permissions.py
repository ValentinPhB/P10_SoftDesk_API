from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions

from softdesk.models import Projects, Contributors


class ProjectRights(permissions.BasePermission):
    """
    Allows access to SAFE_METHODS or lists only to non-object-owner or if they are contributors.
    Allows rights to object-owner or user with author permission | SuperUsers | StaffUser.
    """

    def has_permission(self, request, view,):
        if request.user.is_superuser or request.user.is_staff:
            return True

        try:
            project = Projects.objects.get(pk=view.kwargs.get('pk'))
            if Contributors.objects.filter(
                    user_instance=request.user.id, project_instance=project.id).count() != 0 and (
                    Contributors.objects.filter(user_instance=request.user.id, project_instance=project.id)
            )[0].permission == "AUTEUR":
                return True

            if Contributors.objects.filter(
                    user_instance=request.user.id, project_instance=project.id).count() != 0 and (
                    Contributors.objects.filter(user_instance=request.user.id, project_instance=project.id)
            )[0].permission != "AUTEUR":
                return True

        except ObjectDoesNotExist:
            view.get_queryset()
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        if request.user.id == obj.author_instance.id:
            return True

        if (
            Contributors.objects.filter(
                user_instance=request.user.id, project_instance=obj.id
            ).count()
        ) != 0 and ((Contributors.objects.filter(
            user_instance=request.user.id, project_instance=obj.id)
                            )[0].permission == "AUTEUR" or
                    request.method in permissions.SAFE_METHODS):
            return True


class ContributorsRights(permissions.BasePermission):
    """
    Allows access to SAFE_METHODS or lists only to non-object-owner or if they are contributors.
    Allows rights to user with author permission | SuperUsers | StaffUser.
    Only user with permission == AUTEUR can add contributors to a project.
    """

    def has_permission(self, request, view,):
        if request.user.is_superuser or request.user.is_staff:
            return True

        try:
            project = Projects.objects.get(pk=view.kwargs.get('projects_pk'))
            if Contributors.objects.filter(
                user_instance=request.user.id, project_instance=project.id).count() != 0 and (
                    Contributors.objects.filter(user_instance=request.user.id, project_instance=project.id)
                    )[0].permission == "AUTEUR":
                return True

            if Contributors.objects.filter(
                user_instance=request.user.id, project_instance=project.id).count() != 0 and (
                    Contributors.objects.filter(user_instance=request.user.id, project_instance=project.id)
                    )[0].permission != "AUTEUR" and request.method in permissions.SAFE_METHODS:
                return True

        except ObjectDoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        if request.user.id == obj.project_instance.author_instance.id:
            return True
        
        if (
            Contributors.objects.filter(
                user_instance=request.user.id, project_instance=obj.project_instance.id).count()) != 0 and (
                    (Contributors.objects.filter(
                        user_instance=request.user.id, project_instance=obj.project_instance.id)[0].permission
                         ) == "AUTEUR" or request.method in permissions.SAFE_METHODS):
            return True


class IssuesRights(permissions.BasePermission):
    """
    Allows access to SAFE_METHODS or lists only to non-object-owner or if they are contributors.
    Allows rights to object-owner or user with author permission | SuperUsers | StaffUser.
    """

    def has_permission(self, request, view,):
        if request.user.is_superuser or request.user.is_staff:
            return True

        try:
            project = Projects.objects.get(pk=view.kwargs.get('projects_pk'))
            if Contributors.objects.filter(
                user_instance=request.user.id, project_instance=project.id).count() != 0 and (
                    Contributors.objects.filter(user_instance=request.user.id, project_instance=project.id)
                    )[0].permission == "AUTEUR":
                return True

            if Contributors.objects.filter(
                user_instance=request.user.id, project_instance=project.id).count() != 0 and (
                    Contributors.objects.filter(user_instance=request.user.id, project_instance=project.id)
                    )[0].permission != "AUTEUR":
                return True

        except ObjectDoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        if request.user.id == obj.parent_project.author_instance.id:
            return True

        if request.user.id == obj.author_instance.id:
            return True

        if (
            Contributors.objects.filter(
                user_instance=request.user.id, project_instance=obj.parent_project.id).count()) != 0 and (
                    (Contributors.objects.filter(
                        user_instance=request.user.id, project_instance=obj.parent_project.id)
                        )[0].permission == "AUTEUR" or request.method in permissions.SAFE_METHODS):
            return True
        

class CommentsRights(permissions.BasePermission):
    """
    Allows access to SAFE_METHODS or lists only to non-object-owner or if they are contributors.
    Allows rights to object-owner or user with author permission | SuperUsers | StaffUser.
    """

    def has_permission(self, request, view,):
        if request.user.is_superuser or request.user.is_staff:
            return True

        try:
            project = Projects.objects.get(pk=view.kwargs.get('projects_pk'))
            if Contributors.objects.filter(
                user_instance=request.user.id, project_instance=project.id).count() != 0 and (
                    Contributors.objects.filter(
                        user_instance=request.user.id, project_instance=project.id)
            )[0].permission == "AUTEUR":
                return True

            if Contributors.objects.filter(
                user_instance=request.user.id, project_instance=project.id).count() != 0 and (
                    Contributors.objects.filter(
                        user_instance=request.user.id, project_instance=project.id)
            )[0].permission != "AUTEUR":
                return True

        except ObjectDoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        if request.user.id == obj.parent_issue.parent_project.author_instance.id:
            return True

        if request.user.id == obj.author_instance.id:
            return True

        if (
            Contributors.objects.filter(
                user_instance=request.user.id, project_instance=obj.parent_issue.parent_project.id).count()
            ) != 0 and (
                (Contributors.objects.filter(
                    user_instance=request.user.id, project_instance=obj.parent_issue.parent_project.id)
                    )[0].permission == 'AUTEUR' or request.method in permissions.SAFE_METHODS):
            return True
