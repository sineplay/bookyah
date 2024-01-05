from django import template

register = template.Library()

@register.filter(name='weekdays')
def weekdays(value):
	"""
	Converts a list of integers to a comma-separated string of weekday names.
	"""
	weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
	days = [int(day) for day in value.split(',') if day.isdigit()]
	names = [weekdays[day] for day in days]
	return ', '.join(names)
