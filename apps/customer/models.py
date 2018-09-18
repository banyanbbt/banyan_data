from django.db import models
from apps.customer.managers import CustomerManager


class BaseModel(models.Model):
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True


class Customer(BaseModel):
    gateway_account = models.CharField("网关客户账户", max_length=255, db_index=True, null=True, blank=True)
    contact_name = models.CharField("联系人姓名", max_length=255, db_index=True, null=True, blank=True)
    contact_email = models.CharField("联系人邮箱", max_length=255, db_index=True, null=True, blank=True)
    contact_mobile = models.CharField("联系人手机号", max_length=255, db_index=True, null=True, blank=True)
    contact_address = models.CharField("联系人地址", max_length=255, db_index=True, null=True, blank=True)
    company_name = models.CharField("公司名称", max_length=255, db_index=True, null=True, blank=True)
    company_website = models.CharField("公司网址", max_length=255, db_index=True, null=True, blank=True)
    status = models.CharField("状态", max_length=255, null=True, blank=True)

    objects = CustomerManager()

    class Meta:
        db_table = "customers"
        verbose_name = "客户"
        verbose_name_plural = verbose_name

    @classmethod
    def find_by_id(cls, customer_id):
        return cls.objects.filter(id=customer_id).first()


class CustomerInterface(BaseModel):
    customer_id = models.IntegerField("客户ID", db_index=True, null=True, blank=True)
    interface_id = models.IntegerField("接口ID")
    bbn_price = models.DecimalField("单次调用价格(BBN)", max_digits=20, decimal_places=10, null=True, blank=True)
    status = models.CharField("状态", max_length=255)

    class Meta:
        db_table = "customer_interfaces"
        verbose_name = "客户已开通接口"
        verbose_name_plural = verbose_name


class CustomerAttachment(BaseModel):
    customer_id = models.IntegerField("客户ID", db_index=True, null=True, blank=True)
    attachment_id = models.IntegerField("附件ID", db_index=True)
    attachment_type = models.CharField("附件类型", max_length=255, db_index=True, null=True, blank=True)
    status = models.CharField("状态", max_length=255)

    class Meta:
        db_table = "customer_attachments"
        verbose_name = "客户上传附件"
        verbose_name_plural = verbose_name


class CustomerBilling(models.Model):
    customer_id = models.IntegerField("客户ID", db_index=True, null=True, blank=True)
    interface_id = models.IntegerField("接口ID", db_index=True)
    request_date = models.DateTimeField("接口调用日期", db_index=True, null=True, blank=True)
    success_count = models.IntegerField("接口成功调用次数", null=True, blank=True)
    bbn_cost = models.DecimalField("BBN消费数量", max_digits=20, decimal_places=10, null=True, blank=True)
    created = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = "customer_billings"
        verbose_name = "客户接口查询日志报表"
        verbose_name_plural = verbose_name
