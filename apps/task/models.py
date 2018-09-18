from django.db import models
from apps.util.task_type import task_type


class BaseModel(models.Model):
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        abstract = True


class Task(BaseModel):
    """任务"""
    name = models.CharField("任务名称", max_length=255, null=True, blank=True)
    created_by = models.IntegerField("创建人ID", default=6)
    type = models.CharField("类型", choices=task_type, max_length=255, db_index=True, null=True, blank=True)
    description = models.TextField("任务描述", null=True, blank=True)
    img = models.ImageField("图片", upload_to='imgs', null=True, blank=True)
    start_time = models.DateTimeField("开始时间", null=True, blank=True)
    end_time = models.DateTimeField("结束时间", null=True, blank=True)
    max_count = models.IntegerField("最大可领取人数", default=0)
    question_price = models.IntegerField("题目单价", null=True, blank=True)
    received_count = models.IntegerField("已领取人数", default=0)
    is_file_answer = models.BooleanField("答案是否需要上传文件", default=False)

    class Meta:
        db_table = "tasks"
        verbose_name = "任务"
        verbose_name_plural = verbose_name

