# BOOKYAH - Asset Reservation Application
# Copyright (C) 2024 Sineplay Studio, LLC
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# The LICENSE file describes the conditions under which this software
# may be distributed.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms import ValidationError

class AllowedEmailDomain(models.Model):
	domain = models.CharField(max_length=255, unique=True)
	
	def __str__(self):
		return self.domain
		
class AppSetting(models.Model):
	restrict_email_domain = models.BooleanField(default=True, verbose_name="Restrict Email Domain")
	
	def save(self, *args, **kwargs):
		if not self.pk and AppSetting.objects.exists():
			raise ValidationError('There can only be one AppSetting instance')
		return super(AppSetting, self).save(*args, **kwargs)
	
	def __str__(self):
		return "Application Setting"

class CustomUserManager(BaseUserManager):
	"""
	Custom user model manager where email is the unique identifier for
	authentication instead of usernames
	"""
	def create_user(self, email, password, **extra_fields):
		"""
		Create and save a User with the given email and password.
		"""
		if not email:
			raise ValueError(_('The Email field must be set'))
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_superuser(self, email, password, **extra_fields):
		"""
		Create and save a Superuser with the given email and password.
		"""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		
		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Superuser must have is_staff=True.'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(_('Superuser must have is_superuser=True.'))
			
		return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
	first_name = models.CharField(max_length=30, blank=True)
	last_name = models.CharField(max_length=30, blank=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	email_verified = models.BooleanField(default=False)
    # other fields...
	
	objects = CustomUserManager()
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']
	
	def __str__(self):
		return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # other fields like first_name, last_name, etc.

# ... any other models
