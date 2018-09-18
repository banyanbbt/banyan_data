from django.contrib import admin
from apps.customer import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'gateway_account', 'contact_name', 'contact_email', 'contact_mobile', 'contact_address',
                    'company_name', 'company_website', 'status', 'created', 'updated']
    search_fields = ['gateway_account', 'contact_name', 'contact_email', 'contact_mobile', 'company_name']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.CustomerInterface)
class CustomerInterfaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'interface_id', 'bbn_price', 'status', 'created', 'updated']
    search_fields = ['customer_id']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.CustomerAttachment)
class CustomerAttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id',  'attachment_id', 'attachment_type', 'status', 'created', 'updated']
    search_fields = ['customer_id', 'attachment_type']
    list_per_page = 20
    date_hierarchy = 'created'


@admin.register(models.CustomerBilling)
class CustomerBillingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'interface_id', 'request_date', 'success_count', 'bbn_cost', 'created']
    search_fields = ['customer_id']
    list_per_page = 20
    date_hierarchy = 'created'

