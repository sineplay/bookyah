from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.core.signing import Signer
from django.conf import settings
from .models import CustomUser
signer = Signer()

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
	if created: # Only send emails upon creation, not every save
		token = signer.sign(instance.pk)
		verification_url = f"http://localhost:8000/verify_email/?token={token}"
		message = (
			f"Hello {instance.first_name}, welcome to BOOKYAH! Your"
			f"account has been created successfully.\n\n"
			f"Please verify your email using the link below:\n"
			f"{verification_url}\n\n"
			f"Regards,\n"
			f"BOOKYAH"
		)
		send_mail(
			'Welcome to BOOKYAH - Verify your email',
			message,
			settings.DEFAULT_FROM_EMAIL,
			[instance.email],
			fail_silently=False,
		)