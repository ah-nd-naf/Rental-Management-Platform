from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from apps.core.models import BaseModel
from .managers import CustomUserManager

class Role(models.TextChoices):
    LANDLORD = 'LANDLORD', 'Landlord'
    TENANT = 'TENANT', 'Tenant'
    ADMIN = 'ADMIN', 'Admin'

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom User model using email as the primary identifier.
    Inherits id, created_at, updated_at, and is_deleted from BaseModel.
    """
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    
    # Required by Django for auth/admin
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"