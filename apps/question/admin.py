from django.contrib import admin
from apps.question import models


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'task_id', 'name', 'status', 'content', 'question_type', 'has_known_answer',
                    'created', 'updated']
    search_fields = ['id']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'task_id', 'question_id', 'content', 'file', 'status',
                    'reviewer_id', 'created', 'updated']
    search_fields = ['id']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'task_id', 'name', 'option_type', 'example', 'is_required',
                    'position', 'status', 'created', 'updated']
    search_fields = ['id', 'name', 'option_type']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.Attachment)
class AttachAdmin(admin.ModelAdmin):
    list_display = ['id', 'task_id', 'question_id', 'created_by', 'detail_type', 'detail_id', 'file_name',
                    'file_obj', 'status', 'reviewer_id', 'created', 'updated']
    search_fields = ['id', 'file_name']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.KnownAnswer)
class KnownAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_id', 'content', 'created', 'updated']
    search_fields = ['question_id']
    list_per_page = 20
    date_hierarchy = 'created'
