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

from django.db import models, transaction
from django.utils import timezone
from authentication.models import CustomUser
import datetime, uuid

# Create your models here.

class AssetType(models.Model):
	name = models.CharField(max_length=255)
	fa_icon = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class (e.g., 'fas fa-camera')")
	
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
	is_recurring = models.BooleanField(default=False)
	recurrence_type = models.CharField(max_length=10, choices=(('daily', 'Daily'), ('weekly', 'Weekly')), blank=True, null=True)
	recurrence_end_date = models.DateField(blank=True, null=True)  # For weekly and monthly
	recurrence_days = models.CharField(max_length=20, blank=True, null=True)  # To store weekdays for weekly recurrence
	recurrence_interval = models.IntegerField(default=1, blank=True, null=True)  # Days for daily, months for monthly
	series_id = models.UUIDField(default=None, editable=False, null=True, blank=True)
	
	def __str__(self):
		return f'{self.user.email} - {self.asset.name}'
		
	def can_be_cancelled(self):
		return timezone.now() < self.start_time
		
	def cancel(self):
		self.delete()
		
			
def generate_recurring_dates(start_date, end_date, recurrence_type, interval=1, weekdays=None):
	dates = []
	current_date = start_date.date()

	if recurrence_type == 'daily':
		while current_date <= end_date:
			dates.append(current_date)
			current_date += datetime.timedelta(days=1)
			
	elif recurrence_type == 'weekly' and weekdays:
		weekdays = [int(day) for day in weekdays]
		
		start_date_added = False
		
		if current_date.weekday() in weekdays:
			dates.append(current_date)
			start_date_added = True
		
		first_weekday_after_start = min((day for day in weekdays if day >= current_date.weekday()), default=min(weekdays))
		days_until_first_weekday = (first_weekday_after_start - current_date.weekday()) % 7
		current_date += datetime.timedelta(days=days_until_first_weekday)
		
		while current_date <= end_date:
			for day in weekdays:
				week_day_date = current_date + datetime.timedelta(days=(day - current_date.weekday()) % 7)
				if week_day_date <= end_date and (week_day_date != start_date.date() or not start_date_added):
					dates.append(week_day_date)
			current_date += datetime.timedelta(weeks=interval)

	print("Generated dates:", dates)
	return dates
