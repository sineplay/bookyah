from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.core.signing import Signer
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from booking.models import Reservation
from booking.forms import ReservationForm

# Create your views here.
class RegisterView(generic.CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'registration/register.html'
	
def verify_email(request):
	token = request.GET.get('token')
	signer = Signer()
	try:
		user_id = signer.unsign(token)
		user = get_object_or_404(CustomUser, pk=user_id)
		user.email_verified = True
		user.save()
		messages.success(request, 'Your email has been verified.')
		return redirect('login')
	except BadSignature:
		messages.error(request, 'Invalid token provided for email verification.')
		return redirect('verify_email_reminder')
		
def verify_email_reminder(request):
	return render(request, 'authentication/verify_email_reminder.html')
	
def resend_verification_email(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		user = CustomUser.objects.filter(email=email).first()

		if user and not user.email_verified:
			# Resend the verification email
			signer = Signer()
			token = signer.sign(user.pk)
			verification_path = reverse('verify_email') + f"?token={token}"
			verification_url = request.build_absolute_uri(verification_path)

			send_mail(
				'Verify Your Email - BOOKYAH',
				f'Hello {user.first_name}, please verify your email by clicking the following link: {verification_url}',
				settings.DEFAULT_FROM_EMAIL,  # Use your actual email
				[user.email],
				fail_silently=False,
			)
			return render(request, 'authentication/verification_email_resent.html')
		else:
			# User does not exist or is already verified
			return render(request, 'authentication/user_not_found_or_verified.html')

	return render(request, 'authentication/resend_verification_email.html')
	
@login_required
def profile_view(request):
	current_time = timezone.now()
	
	# Get the current user's reservations
	active_reservations = Reservation.objects.filter(
		user=request.user, end_time__gte=current_time, start_time__lte=current_time
	)
	
	upcoming_reservations = Reservation.objects.filter(
		user=request.user, start_time__gt=current_time
	)
	# Archived reservations will be handled in a separate view
	
	context = {
		'active_reservations': active_reservations,
		'upcoming_reservations': upcoming_reservations,
	}
	
	return render(request, 'authentication/profile.html', context)
	
@login_required
def update_profile(request):
	if request.method == 'POST':
		form = CustomUserChangeForm(request.POST, instance=request.user)
		
		if form.is_valid():
			form.save()
			messages.success(request, 'Your profile was successfully updated!')
			return redirect('profile')
	else:
		form = CustomUserChangeForm(instance=request.user)
	
	return render(request, 'authentication/update_profile.html', {'form': form})
	
@login_required
def modify_reservation_view(request, pk):
	try:
		reservation = Reservation.objects.get(pk=pk, user=request.user)
	except Reservation.DoesNotExist:
		return HttpResponse("Reservation not found.", status=404)
		
	if request.method == 'POST':
		form = ReservationForm(request.POST, instance=reservation, asset_type_id=reservation.asset.asset_type_id)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your reservation has been updated.')
			user_email = request.user.email
			formatted_start_time = reservation.start_time.strftime('%B %-d, %Y, %-I:%M%p')
			formatted_end_time = reservation.end_time.strftime('%B %-d, %Y, %-I:%M%p')
			modification_path = reverse('modify_reservation', args=[reservation.id])
			modification_url = request.build_absolute_uri(modification_path)
			cancel_path = reverse('cancel_reservation', args=[reservation.id])
			cancel_url = request.build_absolute_uri(cancel_path)
			
			subject = (
				f"Reservation successfully modified for {reservation.asset} - BOOKYAH"
			)
			
			message = (
				f"Hello {request.user.first_name},\n\n"
				f"This email is to notify you that your reservation for {reservation.asset} "
				f"has been successfully updated.\n"
				f"New start time: {formatted_start_time}\n"
				f"New end time: {formatted_end_time}\n\n"
				f"To modify this reservation again, click the following link:\n"
				f"{modification_url}\n\n"
				f"Need to cancel, instead? Click the following link:\n"
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
			return redirect('profile')
	else:
		form = ReservationForm(instance=reservation, asset_type_id=reservation.asset.asset_type_id)
		
	formatted_start_time = reservation.start_time.strftime('%Y-%m-%dT%H:%M')
	formatted_end_time = reservation.end_time.strftime('%Y-%m-%dT%H:%M')
	
	return render(request, 'booking/reserve_template.html', {
		'form': form,
		'reservation': reservation,
		'formatted_start_time': formatted_start_time,
		'formatted_end_time': formatted_end_time,
		'is_modifying': True
	})

@login_required
def cancel_reservation_view(request, pk):
	reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
	if reservation.can_be_cancelled():
		formatted_start_time = reservation.start_time.strftime('%B %-d, %Y, %-I:%M%p')
		asset = reservation.asset
		reservation.cancel()
		messages.success(request, f"Your reservation for {asset} has been cancelled.")
		user_email = request.user.email
		
		subject = (
			f"Reservation cancelled for {asset} - BOOKYAH"
		)
		
		message = (
			f"Hello {request.user.first_name},\n\n"
			f"This email is to notify you that your reservation for {asset} "
			f"on {formatted_start_time} has been successfully cancelled.\n\n"
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
		return redirect('profile')
	else:
		messages.error(request, "This reservation cannot be cancelled.")
		return redirect('profile')

@login_required
def archived_reservations_view(request):
	current_time = timezone.now()
	archived_reservations = Reservation.objects.filter(
		user=request.user, end_time__lt=current_time
	).order_by('-start_time')
	
	return render(request, 'authentication/archived_reservations.html', {'archived_reservations': archived_reservations})
	
@login_required(login_url='login')
def root_redirect(request):
	return redirect('profile')