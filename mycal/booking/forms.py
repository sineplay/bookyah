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

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Reservation, AssetType, Asset  # Import your Reservation model

class ReservationForm(forms.ModelForm):
	is_recurring = forms.BooleanField(required=False)
	recurrence_type = forms.ChoiceField(choices=(('daily', 'Daily'), ('weekly', 'Weekly')), required=False)
	recurrence_end_date = forms.DateField(required=False)  # For weekly and monthly
	recurrence_days = forms.MultipleChoiceField(choices=[(str(i), day) for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])], required=False, widget=forms.CheckboxSelectMultiple())  # For weekly
	recurrence_interval = forms.IntegerField(required=False)  # Days for daily, months for monthly
	
	def __init__(self, *args, **kwargs):
		asset_type_id = kwargs.pop('asset_type_id', None)
		self.reservation_instance = kwargs.get('instance', None)
		super(ReservationForm, self).__init__(*args, **kwargs)
		if asset_type_id:
			self.fields['asset'].queryset = Asset.objects.filter(asset_type_id=asset_type_id)
		else:
			self.fields['asset'].queryset = Asset.objects.none()
			
		# Make the asset field read-only if it's an update
		if self.reservation_instance:
			self.fields['asset'].disabled = True

	class Meta:
		model = Reservation
		fields = ['asset', 'start_time', 'end_time', 'is_recurring', 'recurrence_type', 'recurrence_end_date', 'recurrence_days', 'recurrence_interval']  # include other relevant fields

		# Here, you can customize how Django renders the form fields,
		# specify field types, widgets, placeholders, classes, and more.
		
		widgets = {
			'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'datetimefield'}),
			'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'datetimefield'}),
		}
	
	def clean(self):
		cleaned_data = super().clean()
		start_time = cleaned_data.get('start_time')
		end_time = cleaned_data.get('end_time')
		current_time = timezone.now()
		
		if start_time and start_time < current_time:
			self.add_error('start_time', 'The start time cannot be in the past.')
		
		if start_time and end_time and end_time <= start_time:
			self.add_error('end_time', 'The end time must be after the start time.')
			
		return cleaned_data
