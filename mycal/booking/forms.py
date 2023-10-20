from django import forms
from .models import Reservation  # Import your Reservation model

class ReservationForm(forms.ModelForm):
	class Meta:
		model = Reservation
		fields = ['asset', 'start_time', 'end_time']  # include other relevant fields

		# Here, you can customize how Django renders the form fields,
		# specify field types, widgets, placeholders, classes, and more.
		
		widgets = {
			'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'datetimefield'}),
			'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'datetimefield'}),
		}

