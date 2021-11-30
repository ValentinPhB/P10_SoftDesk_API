# import jwt
# from datetime import datetime, timedelta

from django.conf import settings
from django.db import models, transaction
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password):
        if email is None:
            raise TypeError("Une adresse email est requise")
        
        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        if email is None:
            raise TypeError("Une adresse email est requise")

        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
    
    def create_staffuser(self, email, first_name, last_name, password):
        if email is None:
            raise TypeError("Une adresse email est requise")

        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = False
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        verbose_name="Prénom", max_length=150)
    last_name = models.CharField(
        verbose_name="Nom de famille", max_length=150)
    email = models.EmailField(
        verbose_name="Email", max_length=150, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name_plural = "Liste des utilisateurs"
        verbose_name = "Utilisateurs"

    def __str__(self):
        return '%s, %s, %s' % (self.first_name, self.last_name, self.email,)

    def get_full_name(self):
        return '%s, %s, %s' % (self.first_name, self.last_name, self.email,)

    def get_short_name(self):
        return '%s, %s' % (self.first_name, self.last_name)

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_email(self):
        return self.email

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    # @property
    # def token(self):
    #     """
    #     Allows us to get a user's token by calling `UserInstance.token` instead of
    #     `user.generate_jwt_token().

    #     The `@property` decorator above makes this possible. `token` is called
    #     a "dynamic property".
    #     """
    #     return self._generate_jwt_token()

    # def _generate_jwt_token(self):
    #     """
    #     Generates a JSON Web Token that stores this user's ID and has an expiry
    #     date set to 7 days.
    #     """
    #     dt = datetime.now() + timedelta(days=7)

    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')

    #     return token.decode('utf-8')
