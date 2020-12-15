from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, first_name, last_name, user_name, email, password, **other_fields):
        """takes in details of user and if valid creates super user

        Args:
            first_name ([type]): [description]
            last_name ([type]): [description]
            user_name ([type]): [description]
            email ([type]): [description]
            password ([type]): [description]

        Raises:
            ValueError: [description]
            ValueError: [description]

        Returns:
            [type]: [description]
        """        
        """
        takes details of the user as input and if all details are valid then it will create superuser profile
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
        """
        takes details of the user as input and if all credentials are valid then it will create user
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