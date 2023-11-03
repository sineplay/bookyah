from django.db import models
from django.utils import timezone
from authentication.models import CustomUser

# Create your models here.

class AssetType(models.Model):
	name = models.CharField(max_length=255)
	
	def __str__(self):
		return self.name

class Asset(models.Model):
	name = models.CharField(max_length=255)
	asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
	description = models.TextField()
	
	def __str__(self):
		return self.name
	
class Reservation(models.Model):
	asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	
	def __str__(self):
		return f'{self.user.email} - {self.asset.name}'
		
	def can_be_cancelled(self):
		return timezone.now() < self.start_time
		
	def cancel(self):
		self.delete()