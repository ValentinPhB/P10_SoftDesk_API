from django.conf import settings
from django.db import models


class Projects(models.Model):
    class Type(models.TextChoices):
        NON_RENSEIGNE = "NON RENSEIGNÉ"
        BACK_END = "BACK-END"
        FRONT_END = "FRONT-END"
        IOS = "IOS"
        ANDROID = "ANDROID"

    author_instance = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="projects_instances", on_delete=models.CASCADE)

    title = models.CharField(verbose_name="Titre", max_length=150, unique=True)
    description = models.CharField(verbose_name="Description", max_length=150)

    type_project = models.CharField(
        verbose_name="Type", choices=Type.choices, max_length=20)

    class Meta:
        verbose_name_plural = "Liste des projets créés"
        verbose_name = "Projet"

    def __str__(self):
        return self.title


class Contributors(models.Model):
    class Role(models.TextChoices):
        CONTRIBUTEUR = "CONTRIBUTEUR"
        AUTEUR = "AUTEUR"

    class Permission(models.TextChoices):
        CONTRIBUTEUR = "CONTRIBUTEUR"
        AUTEUR = "AUTEUR"

    user_instance = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contributors_instances")
    project_instance = models.ForeignKey(
        Projects, on_delete=models.CASCADE, related_name='contributors', null=True)

    permission = models.CharField(
        verbose_name="Permission", choices=Permission.choices,  max_length=20)
    role = models.CharField(verbose_name="Rôle",
                            choices=Role.choices, max_length=20)

    class Meta:
        verbose_name_plural = "Liste des contributions"
        verbose_name = "Contribution"

    def __str__(self):
        return self.user_instance.email


class Issues(models.Model):
    class Priority(models.TextChoices):
        NON_RENSEIGNE = "NON RENSEIGNÉ"
        ÉLEVÉE = "ÉLEVÉE"
        MOYENNE = "MOYENNE"
        FAIBLE = "FAIBLE"

    class Tag(models.TextChoices):
        NON_RENSEIGNE = "NON RENSEIGNÉ"
        BUG = "BUG"
        AMÉLIORATION = "AMÉLIORATION"
        TÂCHE = "TÂCHE"

    class Status(models.TextChoices):
        À_FAIRE = "À FAIRE"
        EN_COURS = "EN COURS"
        TÉRMINÉ = "TÉRMINÉ"

    author_instance = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issues_instances')

    parent_project = models.ForeignKey(
        Projects, on_delete=models.CASCADE, related_name="issues")

    title = models.CharField(verbose_name="Titre", max_length=150, unique=True)
    description = models.CharField(verbose_name="Description", max_length=150)
    created_time = models.DateTimeField(
        verbose_name="date de publication", auto_now_add=True)

    priority = models.CharField(
        verbose_name="Priorité", choices=Priority.choices, max_length=20)
    tag = models.CharField(verbose_name="Balise",
                           choices=Tag.choices, max_length=20)
    status = models.CharField(verbose_name="Status",
                              choices=Status.choices, max_length=20)

    class Meta:
        verbose_name_plural = "Liste des Problèmes notifiés"
        verbose_name = "Problème notifié"

    def __str__(self):
        return '%s PRIORITÉ %s, STATUS %s' % (self.title, self.priority, self.status)


class Comments(models.Model):
    author_instance = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="comments_instances", on_delete=models.CASCADE)
    parent_issue = models.ForeignKey(
        Issues, on_delete=models.CASCADE, related_name="comments")

    description = models.CharField(verbose_name="Description", max_length=150)
    created_time = models.DateTimeField(
        verbose_name="date de publication", auto_now_add=True)

    class Meta:
        verbose_name_plural = "Liste des commentaires"
        verbose_name = "Commentaire"

    def __str__(self):
        return self.description
