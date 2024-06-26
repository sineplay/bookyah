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

from django.conf import settings
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .forms import ReservationForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from .models import AssetType, Asset, Reservation, generate_recurring_dates
from .utils import send_reservation_notification
import datetime, uuid

# Create your views here.

def check_conflicts(start_time, end_time, asset_id):
	conflicts = Reservation.objects.filter(
		Q(asset_id=asset_id),
		Q(start_time__lt=end_time, end_time__gt=start_time)
	)
	return conflicts

@login_required
def select_asset_type(request):
	if not request.user.email_verified:
		return redirect('verify_email_reminder')
	asset_types = AssetType.objects.all()
	return render(request, 'booking/asset_type_selection.html', {'asset_types': asset_types})
	
@login_required
def create_reservation(request, asset_type_id=None):
	if not request.user.email_verified:
		return redirect('verify_email_reminder')
	asset_type = AssetType.objects.get(id=asset_type_id)
	assets = Asset.objects.none() # Default to no assets
	
	if asset_type_id:
		assets = Asset.objects.filter(asset_type_id=asset_type_id)
	if request.method == 'POST':
		form = ReservationForm(request.POST, asset_type_id=asset_type_id)
		if form.is_valid():
			asset = form.cleaned_data['asset']
			start_time = form.cleaned_data['start_time']
			end_time = form.cleaned_data['end_time']
			series_id = None
			
			# Check for overlapping reservations
			overlapping_reservations = Reservation.objects.filter(
				asset=asset,
				start_time__lt=end_time,
				end_time__gt=start_time
			)
			if overlapping_reservations.exists():
				messages.error(request, 'This asset is already reserved during the requested time.')
				return render(request, 'booking/reserve_template.html', {'form': form, 'asset_type_name': asset_type.name })
			
			if form.cleaned_data['is_recurring']:
				# messages.info(request,"The recurring event code was triggered.")
				recurrence_days = [int(day) for day in form.cleaned_data.get('recurrence_days', [])]
				recurring_dates = generate_recurring_dates(
					start_time,
					form.cleaned_data['recurrence_end_date'],
					form.cleaned_data['recurrence_type'],
					interval=1, # Hardcoded interval until we have support for intervals
					weekdays=recurrence_days
				)
				
				conflicts = []
				for date in recurring_dates:
					new_start = datetime.datetime.combine(date, start_time.time())
					new_end = datetime.datetime.combine(date, end_time.time())
					
					if check_conflicts(new_start, new_end, form.cleaned_data['asset'].id).exists():
						conflicts.append(new_start)
						
					if len(conflicts) >= 10:
						break
				
				if conflicts:
					conflict_dates = ', '.join([date.strftime("%Y-%m-%d %H:%M") for date in conflicts])
					messages.error(request, f"Cannot create recurring reservation due to conflicts on these dates: {conflict_dates}. Please choose different times or modify the recurrence pattern.")
					
					assets = Asset.objects.filter(asset_type_id=asset_type_id) if asset_type_id else Asset.objects.none()
					
					return render(request, 'booking/reserve_template.html', {
					'form': form,
					'asset_type_name': asset_type.name,
					'assets': assets,
				})
				else:
					series_id = uuid.uuid4()
					first_reservation = None
					with transaction.atomic():
						for date in recurring_dates:
							new_start = datetime.datetime.combine(date, start_time.time())
							new_end = datetime.datetime.combine(date, end_time.time())
							reservation = Reservation.objects.create(
								asset=form.cleaned_data['asset'],
								start_time=new_start,
								end_time=new_end,
								user=request.user,
								series_id=series_id,
								is_recurring=form.cleaned_data['is_recurring'],
								recurrence_type=form.cleaned_data['recurrence_type'],
								recurrence_end_date=form.cleaned_data['recurrence_end_date'],
								recurrence_days=','.join(map(str, recurrence_days)) if recurrence_days else ''
							)
							if not first_reservation:
								first_reservation = reservation
					if first_reservation:
						formatted_start_time = first_reservation.start_time.strftime('%B %-d, %Y, %-I:%M%p')
						formatted_end_time = first_reservation.end_time.strftime('%B %-d, %Y, %-I:%M%p')
						formatted_end_date = first_reservation.recurrence_end_date.strftime('%B %-d, %Y')
						user_email = request.user.email
						profile_path = reverse('profile')
						profile_url = request.build_absolute_uri(profile_path)
						cancel_path = reverse('cancel_series', args=[series_id])
						cancel_url = request.build_absolute_uri(cancel_path)
						subject = (
							f"Reservation successfully created for {reservation.asset} - BOOKYAH"
						)
			
						message = (
							f"Hello {request.user.first_name},\n\n"
							f"This email is to notify you that your reservation series for {first_reservation.asset} "
							f"has been successfully created.\n"
							f"Start time: {formatted_start_time}\n"
							f"End time: {formatted_end_time}\n"
							f"Recurrence type: {first_reservation.recurrence_type}\n"
							f"Series end date: {formatted_end_date}\n\n"
							f"To modify or cancel a single reservation, visit your profile:\n"
							f"{profile_url}\n\n"
							f"To cancel the series, click the following link:\n"
							f"{cancel_url}\n\n"
							"Regards,\n"
							"BOOKYAH"
						)
			
						send_mail(
							subject,
							message,
							settings.DEFAULT_FROM_EMAIL,  # Use your DEFAULT_FROM_EMAIL
							[user_email],  # List of recipient(s)
							fail_silently=False,
						)
						return redirect('reserve-success')
				
			reservation = form.save(commit=False)
			reservation.user = request.user
			reservation.series_id = series_id
			reservation.save()
			user_email = request.user.email
			formatted_start_time = reservation.start_time.strftime('%B %-d, %Y, %-I:%M%p')
			formatted_end_time = reservation.end_time.strftime('%B %-d, %Y, %-I:%M%p')
			modification_path = reverse('modify_reservation', args=[reservation.id])
			modification_url = request.build_absolute_uri(modification_path)
			cancel_path = reverse('cancel_reservation', args=[reservation.id])
			cancel_url = request.build_absolute_uri(cancel_path)
			
			subject = (
				f"Reservation successfully created for {reservation.asset} - BOOKYAH"
			)
			
			message = (
				f"Hello {request.user.first_name},\n\n"
				f"This email is to notify you that your reservation for {reservation.asset} "
				f"has been successfully created.\n"
				f"Start time: {formatted_start_time}\n"
				f"End time: {formatted_end_time}\n\n"
				f"To modify this reservation, click the following link:\n"
				f"{modification_url}\n\n"
				f"Need to cancel? Click the following link:\n"
				f"{cancel_url}\n\n"
				"Regards,\n"
				"BOOKYAH"
			)
			
			send_mail(
				subject,
				message,
				settings.DEFAULT_FROM_EMAIL,  # Use your DEFAULT_FROM_EMAIL
				[user_email],  # List of recipient(s)
				fail_silently=False,
			)
			return redirect('reserve-success')
	else:
		form = ReservationForm(asset_type_id=asset_type_id)
		assets = Asset.objects.filter(asset_type_id=asset_type_id) if asset_type_id else Asset.objects.none()
		# form.fields['asset'].queryset = Asset.objects.none()
		
	return render(request, 'booking/reserve_template.html', {
		'form': form,
		'asset_type_name': asset_type.name,
		'assets': assets,
		'is_modifying': False
	})

@login_required
def reserve_success(request):
	return render(request, 'booking/reserve_success.html', {})
	
	
@login_required
def reservation_data(request):
	asset_id = request.GET.get('asset_id')
	
	if asset_id:
		reservations = Reservation.objects.filter(asset_id=asset_id)
	else:
		reservations = Reservation.objects.all()
	
	reservation_data = [{
		'title': reservation.asset.name,
		'id': reservation.id,
		'start': reservation.start_time.isoformat(),
		'end': reservation.end_time.isoformat(),
		# More fields as required by FullCalendar
	} for reservation in reservations]

	return JsonResponse(reservation_data, safe=False)
	
@staff_member_required
def admin_reservation_data(request):
	asset_type_id = request.GET.get('asset_type_id')
	
	if asset_type_id:
		reservations = Reservation.objects.filter(asset__asset_type_id=asset_type_id)
	else:
		reservations = Reservation.objects.all()
	
	reservation_data = [{
		'title': f'{reservation.user.email} - {reservation.asset.name}',
		'id': reservation.id,
		'start': reservation.start_time.isoformat(),
		'end': reservation.end_time.isoformat(),
	} for reservation in reservations]
	
	return JsonResponse(reservation_data, safe=False)
	
@staff_member_required
def admin_calendar_view(request):
	asset_types = AssetType.objects.all()
	return render(request, 'booking/admin_calendar.html', {'asset_types': asset_types})
	
@staff_member_required
def view_series(request, series_id):
	series_reservations = get_list_or_404(Reservation, series_id=series_id)
	return render(request, 'admin/view_series.html', {'reservations': series_reservations, 'series_id':series_id})

@staff_member_required
def delete_series(request, series_id):
	if request.method == 'POST':
		reservation = Reservation.objects.filter(series_id=series_id).first()
		if not reservation:
			messages.error(request, "No reservations found in this series.")
			return redirect(reverse('admin:view_series', args=[series_id]))
		
		user = reservation.user

		Reservation.objects.filter(series_id=series_id).delete()
		
		if reservation.start_time > timezone.now():
			send_reservation_notification(request, user, reservation, 'cancelled')

		messages.success(request, "The entire series has been cancelled.")
		return HttpResponseRedirect(reverse('admin:booking_reservation_changelist'))
	return HttpResponseRedirect(reverse('admin:view_series', args=[series_id]))