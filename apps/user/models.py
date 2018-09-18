from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from apps.user.managers import UserProfileManager, UserApplyInterfaceInfoManager
from apps.user.model_status import USER_TYPE_STATUS, USER_TASK_STATUS
from apps.customer.models import Customer


class BaseModel(models.Model):
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        abstract = True


class UserProfile(AbstractUser):
    """用户"""
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        help_text=_('150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    mobile = models.CharField("手机号", db_index=True, max_length=255, null=True, blank=True)
    bbn_count = models.IntegerField("BBN数量", default=0)
    is_valid_email = models.BooleanField("邮箱是否验证", default=False)
    user_type = models.CharField("用户类型", max_length=255, db_index=True, null=True, blank=True)
    customer_id = models.IntegerField("客户ID", db_index=True, null=True, blank=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    objects = UserProfileManager()

    class Meta:
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email


class UserReward(BaseModel):
    """用户奖励"""
    user_id = models.IntegerField("用户id", db_index=True, null=True, blank=True)
    bbn_count = models.IntegerField("收支", null=True, blank=True)
    reward_type = models.CharField("奖励类型", max_length=255, db_index=True, null=True, blank=True)
    reason = models.CharField("奖励原因", max_length=255, null=True, blank=True)

    class Meta:
        db_table = "user_rewards"
        verbose_name = "用户奖励"
        verbose_name_plural = verbose_name


class UserWithdraw(BaseModel):
    """提现记录"""
    user_id = models.IntegerField("用户id", db_index=True, null=True, blank=True)
    bbn_count = models.IntegerField("提现数额", null=True, blank=True)
    wallet_address = models.CharField("提现地址", max_length=255, null=True, blank=True)
    status = models.CharField("提现状态", max_length=255, null=True, blank=True)

    class Meta:
        db_table = "user_withdraws"
        verbose_name = "提现记录"
        verbose_name_plural = verbose_name


class UserTask(BaseModel):
    """用户领取任务"""
    user_id = models.IntegerField("用户id", db_index=True, null=True, blank=True)
    task_id = models.IntegerField("任务id", db_index=True, null=True, blank=True)
    finished_count = models.IntegerField("完成数量", default=0)
    passed_count = models.IntegerField("审核通过条数", db_index=True, default=0)
    passed_reward_count = models.IntegerField("奖励数量", default=0)
    is_file_answer = models.BooleanField("答案是否需要上传文件", default=False)
    status = models.CharField("状态", choices=USER_TASK_STATUS, max_length=255, db_index=True, null=True, blank=True)

    class Meta:
        db_table = "user_tasks"
        verbose_name = "用户领取任务"
        verbose_name_plural = verbose_name


class Feedback(BaseModel):
    """用户反馈"""
    contact_name = models.CharField("联系人姓名", max_length=255, null=True, blank=True)
    company_name = models.CharField("公司", max_length=255, null=True, blank=True)
    contact_mobile = models.CharField("手机号", max_length=255, null=True, blank=True)
    contact_email = models.CharField("邮箱", max_length=255, null=True, blank=True)
    feedback_content = models.TextField("反馈", null=True, blank=True)

    class Meta:
        db_table = "feedback"
        verbose_name = "用户反馈"
        verbose_name_plural = verbose_name


class UserValidateCode(models.Model):
    """用户验证码"""
    user_id = models.IntegerField("用户id", null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name='发送邮箱')
    code = models.CharField(max_length=255)
    is_used = models.BooleanField("验证码是否被使用", default=False)
    created = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "validate_codes"
        verbose_name = "用户验证码"
        verbose_name_plural = verbose_name


class UserApplyInterfaceInfo(BaseModel):
    """用户申请调用信息"""
    product_name = models.CharField("产品名", max_length=255, null=True, blank=True)
    contact_name = models.CharField("联系人姓名", max_length=255, null=True, blank=True)
    contact_mobile = models.CharField("手机号", max_length=255, null=True, blank=True)
    expected_dosage = models.CharField("预计用量", max_length=255, null=True, blank=True)

    objects = UserApplyInterfaceInfoManager()

    class Meta:
        db_table = "apply_interface_info"
        verbose_name = "用户申请调用信息"
        verbose_name_plural = verbose_name


class ReviewAnswer(BaseModel):
    """审核记录"""
    answer_id = models.IntegerField()
    reviewer_id = models.CharField("审核人id", max_length=255, db_index=True, null=True, blank=True)
    status = models.CharField("状态")


class BudgetInfo(BaseModel):
    """奖励信息"""
    action = models.CharField("行为", max_length=255, null=True, blank=True)
    change_count = models.IntegerField("变动数量", null=True, blank=True)

