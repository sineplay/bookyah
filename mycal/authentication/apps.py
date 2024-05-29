from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    
    def ready(self):
        import authentication.signals
        from .models import AppSetting
#        AppSetting.objects.get_or_create(pk=1)