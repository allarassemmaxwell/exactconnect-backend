# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from uuid import uuid4
import os
from datetime import datetime




def path_and_rename(instance, filename):
    """
    Generates a file path based on the current year/month and model pk or UUID for filename.
    """
    upload_to = '{}/{}/'.format(datetime.now().year, datetime.now().month)
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


# CREATE USERMANAGER 
class UserManager(BaseUserManager):
    """
    Custom manager for user creation with roles: user, staff, superuser.
    Provides methods to create regular users, staff users, and superusers.
    """
    use_in_migrations = True
    def save_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("L'e-mail donné doit être défini"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self.save_user(email, password, **extra_fields)

    def create_staffuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = False
        
        return self.save_user(email, password, **extra_fields) 

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("is_superuser devrait être vrai"))
        extra_fields['is_staff'] = True
        return self.save_user(email, password, **extra_fields) 
    

class User(AbstractBaseUser, PermissionsMixin):
    """
    Represents a system user with personal info, contact details, and role.
    Includes fields like name, email, gender, city, neighborhood, and account status.
    """
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, unique=True, validators = [validators.EmailValidator()])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email


class Product(models.Model):
    """
    Represents a product fetched from an external API, stored in the local database.
    """
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        """
        Returns a readable string representing the order: 'username - product title'.
        """
        return self.title

class Order(models.Model):
    """
    Stores the relationship between a user and a product order.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __str__(self):
        """
        Returns a readable string representing the order: 'username - product title'.
        """
        return f"{self.user.username} - {self.product.title}"


    def total_price(self):
        """
        Calculates the total price for this order.
        """
        return self.quantity * self.product.price
