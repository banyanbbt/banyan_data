from django.db import models


class ProductCategory(models.Model):
    parent_id = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'product_category'

    def __str__(self):
        return self.name


class Product(models.Model):
    product = models.CharField(primary_key=True, max_length=16)
    category_id = models.IntegerField(blank=True, null=True)
    fee_type = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    service_method = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    source = models.CharField(max_length=16)
    status = models.BooleanField()
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'product'

    def __str__(self):
        return self.name


class AccountProduct(models.Model):
    account = models.CharField(primary_key=True, max_length=16)
    product = models.CharField(max_length=16)
    highest_price = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    lowest_price = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    bbn_price = models.DecimalField("单次调用价格(BBN)", max_digits=20, decimal_places=10, null=True, blank=True)
    limit_count = models.IntegerField()
    used_count = models.IntegerField()
    effective_at = models.DateTimeField(blank=True, null=True)
    expire_at = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField()
    created_by = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    product_name = models.CharField(max_length=64, blank=True, null=True)
    category_name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'account_product'
        unique_together = (('account', 'product'),)

    def __str__(self):
        return '%s, %s' % (self.account, self.product)




