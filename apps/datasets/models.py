from django.db import models


class Datasets(models.Model):
    name = models.CharField("数据集名称", max_length=255, null=True, blank=True)
    avatar = models.ImageField("图片", upload_to='imgs', null=True, blank=True)
    bbn_price = models.IntegerField("BBN价格", default=0, null=True, blank=True)
    description = models.TextField("数据集描述", null=True, blank=True)
    release_at = models.DateTimeField("发布时间", null=True, blank=True)
    download_count = models.IntegerField("已下载次数", default=0, null=True, blank=True)
    dataset_type = models.CharField("数据集类型", max_length=255, db_index=True, null=True, blank=True)
    status = models.CharField("数据集状态", max_length=255, null=True, blank=True)
    created_by = models.IntegerField("创建人ID", default=0, null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "datasets"
        verbose_name = "数据集"
        verbose_name_plural = verbose_name
