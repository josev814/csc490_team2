from random import randint
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """
    Class that handles the management of a user
    """
    
    def create_user(self, email:str, password:str, **kwargs):
        """
        Use this to create a regular user
        """
        if password is None:
            raise TypeError('Users must have a password.')
        if email is None:
            raise TypeError('Users must have an email.')

        user = self.model(
            email=self.normalize_email(email),
            token = self.__generate_user_token(),
            isactive = False
        )
        user.set_password(password)

        user.save(using=self._db)
        return user
    
    def __generate_user_token(self) -> str:
        """
        Generates a user token that's used for validation
        The token must be validated prior to an account being marked active
        """
        rand = str(randint(000000, 999999))
        while len(rand) < 6:
            rand = '0' + rand
        return rand

    def create_superuser(self, username, email, password):
        """
        Create and return a User with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True,  null=True, blank=True)
    token = models.CharField(db_index=True,  max_length=6, unique=True,  null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"
