from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True, null=False)
    firstName = models.CharField(max_length=255, null=False)
    lastName = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=15, null=True, blank=True)
    objects = UserManager()

    groups = models.ManyToManyField(Group, related_name='user_accounts')
    user_permissions = models.ManyToManyField(
        Permission, related_name='user_accounts')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def get_full_name(self):
        return f'{self.firstName}-{self.lastName}' 

    
    def __str__(self):
        return str(self.email)
    

class Organization(models.Model):
    org_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1225, null=False)
    description = models.CharField(max_length=2000, null=True)
    users = models.ManyToManyField(User, related_name='organizations')

    def __str__(self):
        return self.name
