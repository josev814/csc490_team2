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
            is_active = True
        )
        user.set_password(password)

        user.save(using=self._db)
        return user
    
    def __generate_user_token(self) -> str:
        """
        Generates a user token that's used for validation
        The token must be validated prior to an account being marked active
        """
        self.rand = str(randint(000000, 999999))
        if len(self.rand) < 6:
            self.__expand_user_token_length()
        return self.rand

    def __expand_user_token_length(self) -> str:
        while len(self.rand) < 6:
            self.rand = '0' + self.rand

    def create_superuser(self, email, password):
        """
        Create and return a User with superuser (admin) permissions.
        """
        # Email and password are validated in create_user
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True,  null=False, blank=False)
    token = models.CharField(db_index=True,  max_length=6, unique=True,  null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return f"{self.email, self.is_active, self.last_login}"
