import jsonfield
from django.db import models
from apps.interface.managers import InterfaceManager, InterfaceParamManager, InterfaceExampleManager


class BaseModel(models.Model):
    created = models.DateTimeField('创建时间', auto_now_add=True)
    updated = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True


class InterfaceProfile(BaseModel):
    """接口信息"""
    name = models.CharField("接口名称", max_length=255, db_index=True)
    img = models.ImageField("接口图片")
    category = models.CharField("接口种类", max_length=255, null=True, blank=True)
    price = models.IntegerField("每次调用价格(BBN)")
    info = models.TextField("描述")
    desc = models.CharField("接口介绍", max_length=255)
    scene = models.CharField("适用场景", max_length=255)

    objects = InterfaceManager()

    class Meta:
        db_table = 'interface_profile'
        verbose_name = "接口"
        verbose_name_plural = verbose_name


class InterfaceParam(BaseModel):
    """接口参数"""
    interface_id = models.IntegerField("接口id")
    is_res = models.BooleanField("是否为返回参数", default=False)
    name = models.CharField("参数名", max_length=255)
    p_type = models.CharField("参数类型", max_length=255, null=True, blank=True)
    demand = models.CharField("输入要求", max_length=255, null=True, blank=True)
    info = models.CharField("说明", max_length=255)

    objects = InterfaceParamManager()

    class Meta:
        db_table = 'interface_params'
        verbose_name = "接口参数"
        verbose_name_plural = verbose_name


class InterfaceExample(BaseModel):
    """接口示例"""
    interface_id = models.IntegerField("接口id")
    is_res = models.BooleanField("是否为返回示例", default=False)
    content = jsonfield.JSONField("示例内容")
    e_type = models.CharField("类型", max_length=255)

    objects = InterfaceExampleManager()

    class Meta:
        db_table = 'interface_examples'
        verbose_name = "接口示例（请求，返回）"
        verbose_name_plural = verbose_name
