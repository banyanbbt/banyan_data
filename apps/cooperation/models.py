from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True


class DataSourceCooperationInfo(BaseModel):
    """数据源合作信息"""
    desc = models.TextField("数据描述", null=True, blank=True)
    data_amount = models.IntegerField("数据量(条)", null=True, blank=True)
    data_fields = models.TextField("数据字段", null=True, blank=True)
    contact_name = models.CharField("联系人姓名", max_length=255, null=True, blank=True)
    contact_mobile = models.CharField("联系人手机号", max_length=255, null=True, blank=True)

    class Meta:
        db_table = "data_source_cooperation_info"
        verbose_name = "数据源合作信息"
        verbose_name_plural = verbose_name

