from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
	pass
	# To be worked on

class CustomUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    # other fields...
	
	objects = CustomUserManager()
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

# Any additional models related to the authentication app
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # other fields like first_name, last_name, etc.

# ... any other models
