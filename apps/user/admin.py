from django.contrib import admin
from apps.user import models


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_type', 'email', 'password', 'mobile', 'bbn_count', 'is_staff', 'is_superuser', 'is_valid_email',
                    'last_login', 'customer_id', 'date_joined', 'updated']
    search_fields = ['id', 'email']
    list_per_page = 20
    date_hierarchy = 'date_joined'


@admin.register(models.UserReward)
class UserRewardAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'bbn_count', 'reward_type', 'reason', 'created', 'updated']
    search_fields = ['id', 'reward_type']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.UserWithdraw)
class UserWithdrawAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'bbn_count', 'wallet_address', 'status', 'created', 'updated']
    search_fields = ['id', 'status']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'task_id', 'passed_count', 'passed_reward_count',
                    'status', 'finished_count', 'is_file_answer', 'created', 'updated']
    search_fields = ['id', 'status']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'contact_name', 'company_name', 'contact_mobile', 'contact_email',
                    'feedback_content', 'created', 'updated']
    search_fields = ['id', 'contact_name']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.UserValidateCode)
class UserValidateCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'email', 'code', 'is_used', 'created']
    search_fields = ['user_id', 'email']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.UserApplyInterfaceInfo)
class UserValidateCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'contact_name', 'contact_mobile', 'expected_dosage', 'created', 'updated']
    search_fields = ['product_name', 'contact_name', 'contact_mobile']
    list_per_page = 20
    date_hierarchy = 'created'
