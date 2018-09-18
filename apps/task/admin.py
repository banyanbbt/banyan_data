from django.contrib import admin
from apps.task import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_by',  'type', 'description', 'img', 'start_time', 'end_time',
                    'question_price', 'received_count', 'max_count', 'is_file_answer', 'created', 'updated']
    search_fields = ['id', 'name', 'type']
    list_per_page = 20
    date_hierarchy = 'created'
