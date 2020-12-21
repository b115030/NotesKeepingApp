from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, first_name, last_name, user_name, email, password, **other_fields):
        """takes in details of user and if valid creates super user

        Args:
            first_name (string): first name of the user
            last_name (string): last name of the user
            user_name (string): user name of the user
            email (string): email of the user
            password (string): password of the user

        Raises:
            ValueError: Superuser must be is_staff=True
            ValueError: Superuser must be assigned to is_superuser=True

        Returns:
            json: user objects
        """       
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_verified', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(first_name, last_name, user_name, email, password, **other_fields)

    def create_user(self, first_name, last_name, user_name, email, password, **other_fields):
        """ takes details of the user as input, if valid creates user

        Raises:
            ValueError: must provide an email address

        Returns:
            object: user object
        """        
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, user_name=user_name, email=email,
                          password=password, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'