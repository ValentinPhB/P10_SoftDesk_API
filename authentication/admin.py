from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import Group

from authentication.models import User
from softdesk.models import Projects, Contributors, Issues, Comments


class ProjectsInLine(admin.TabularInline):
    model = Projects
    fk_name = 'author_instance'
    extra = 0

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"


class ContributorsInLine(admin.TabularInline):
    model = Contributors
    fk_name = 'user_instance'
    extra = 0

    class Meta:
        verbose_name = "Contribution"
        verbose_name_plural = "Contributions"


class IssuesInLine(admin.TabularInline):
    model = Issues
    fk_name = 'author_instance'
    extra = 0

    class Meta:
        verbose_name = "Problème notifié"
        verbose_name_plural = "Problèmes notifiés"


class CommentsInLine(admin.TabularInline):
    model = Comments
    fk_name = 'author_instance'
    extra = 0

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email',
                    'is_active', 'is_staff', 'is_superuser', 'date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')
                }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    inlines = [ProjectsInLine, ContributorsInLine,
               IssuesInLine, CommentsInLine]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
