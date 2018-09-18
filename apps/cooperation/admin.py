from django.contrib import admin
from apps.cooperation import models


@admin.register(models.DataSourceCooperationInfo)
class DataSourceCooperationInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'desc', 'data_amount', 'data_fields', 'contact_name',
                    'contact_mobile', 'created', 'updated']
    search_fields = ['contact_name']
    list_per_page = 20
    date_hierarchy = 'created'
