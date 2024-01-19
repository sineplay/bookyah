from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from .models import AllowedEmailDomain, AppSetting, CustomUser, UserProfile

admin.site.register(CustomUser)
admin.site.register(UserProfile)

@admin.register(AllowedEmailDomain)
class AllowedEmailDomainAdmin(admin.ModelAdmin):
	list_display = ('domain',)
	search_fields = ('domain',)
	
@admin.register(AppSetting)
class AppSettingAdmin(admin.ModelAdmin):
	list_display = ('restrict_email_domain',)
	
	def has_add_permission(self, request, obj=None):
		return not AppSetting.objects.exists()
		
	def has_delete_permission(self, request, obj=None):
		return False
		
	def response_change(self, request, obj):
		if "_continue" in request.POST:
			return super().response_change(request, obj)
		else:
			return HttpResponseRedirect('/admin/')
			
	def get_urls(self):
		urls = super().get_urls()
		custom_urls = [
			path('edit/', self.admin_site.admin_view(self.edit), name='appsetting_edit'),
		]
		return custom_urls + urls
	
	def edit(self, request):
		obj, created = AppSetting.objects.get_or_create(pk=1)
		return HttpResponseRedirect(
			f'/admin/{self.model._meta.app_label}/{self.model._meta.model_name}/{obj.pk}/change/'
		)
		
	def changelist_view(self, request, extra_context=None):
		# If there's no instance, create one and redirect to its change form
		# If there's an instance, redirect to its change form
		obj, created = AppSetting.objects.get_or_create(pk=1)
		return HttpResponseRedirect(
			f'/admin/{self.model._meta.app_label}/{self.model._meta.model_name}/{obj.pk}/change/'
		)

