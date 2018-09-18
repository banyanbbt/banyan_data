from django.contrib import admin
from apps.interface import models


@admin.register(models.InterfaceProfile)
class InterfaceProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'img', 'category', 'price', 'info', 'desc', 'scene',
                    'created', 'updated']
    search_fields = ['name']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.InterfaceParam)
class InterfaceParamAdmin(admin.ModelAdmin):
    list_display = ['id', 'interface_id', 'is_res', 'name', 'p_type', 'demand', 'info',
                    'created', 'updated']
    search_fields = ['interface_id', 'name']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.InterfaceExample)
class InterfaceParamAdmin(admin.ModelAdmin):
    list_display = ['id', 'interface_id', 'is_res', 'content', 'e_type',
                    'created', 'updated']
    search_fields = ['interface_id']
    list_per_page = 20
    date_hierarchy = 'created'
