from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ReservationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AssetType, Asset, Reservation

# Create your views here.

@login_required
def select_asset_type(request):
	asset_types = AssetType.objects.all()
	return render(request, 'booking/asset_type_selection.html', {'asset_types': asset_types})
	
def create_reservation(request, asset_type_id):
	asset_type = AssetType.objects.get(id=asset_type_id)
	if request.method == 'POST':
		form = ReservationForm(request.POST, asset_type_id=asset_type_id)
		if form.is_valid():
			asset = form.cleaned_data['asset']
			start_time = form.cleaned_data['start_time']
			end_time = form.cleaned_data['end_time']
			
			# Check for overlapping reservations
			overlapping_reservations = Reservation.objects.filter(
				asset=asset,
				start_time__lt=end_time,
				end_time__gt=start_time
			)
			if overlapping_reservations.exists():
				messages.error(request, 'This asset is already reserved during the requested time.')
				return render(request, 'booking/reserve_template.html', {'form': form, 'asset_type_name': asset_type.name })
				
			reservation = form.save(commit=False)
			reservation.user = request.user
			reservation.save()
			return redirect('reserve-success')
	else:
		form = ReservationForm(asset_type_id=asset_type_id)
		# form.fields['asset'].queryset = Asset.objects.none()
		
	return render(request, 'booking/reserve_template.html', {
		'form': form,
		'asset_type_name': asset_type.name
	})

def reserve_success(request):
	return render(request, 'booking/reserve_success.html', {})
	
	
def reservation_data(request):
	asset_id = request.GET.get('asset_id')
	
	if asset_id:
		reservations = Reservation.objects.filter(asset_id=asset_id)
	else:
		reservations = Reservation.objects.all()
	
	reservation_data = [{
		'title': reservation.asset.name,
		'start': reservation.start_time.isoformat(),
		'end': reservation.end_time.isoformat(),
		# More fields as required by FullCalendar
	} for reservation in reservations]

	return JsonResponse(reservation_data, safe=False)
