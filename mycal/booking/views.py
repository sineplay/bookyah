from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ReservationForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.urls import reverse
from .models import AssetType, Asset, Reservation, generate_recurring_dates
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
					with transaction.atomic():
						for date in recurring_dates:
							new_start = datetime.datetime.combine(date, start_time.time())
							new_end = datetime.datetime.combine(date, end_time.time())
							Reservation.objects.create(
								asset=form.cleaned_data['asset'],
								start_time=new_start,
								end_time=new_end,
								user=request.user,
								series_id=series_id,
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
