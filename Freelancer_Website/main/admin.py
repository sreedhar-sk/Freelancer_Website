from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *
 
@admin.register(service_provider_info) 
@admin.register(ticket_info) 
class ViewAdmin(ImportExportModelAdmin):
	pass

