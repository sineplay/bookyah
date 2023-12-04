from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Reservation, AssetType, Asset  # Import your Reservation model

class ReservationForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		asset_type_id = kwargs.pop('asset_type_id', None)
		super(ReservationForm, self).__init__(*args, **kwargs)
		if asset_type_id:
			self.fields['asset'].queryset = Asset.objects.filter(asset_type_id=asset_type_id)
		else:
			self.fields['asset'].queryset = Asset.objects.none()

	class Meta:
		model = Reservation
		fields = ['asset', 'start_time', 'end_time']  # include other relevant fields

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
