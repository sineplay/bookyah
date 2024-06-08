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

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from import_export.admin import ImportExportModelAdmin
from .resources import CustomUserResource
from .models import AllowedEmailDomain, AppSetting, CustomUser, UserProfile

# admin.site.register(CustomUser)
admin.site.register(UserProfile)

class CustomUserAdmin(ImportExportModelAdmin):
	resource_class = CustomUserResource
	list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'email_verified')
	search_fields = ('email', 'first_name', 'last_name')

# admin.site.unregister(CustomUser)

admin.site.register(CustomUser, CustomUserAdmin)

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

