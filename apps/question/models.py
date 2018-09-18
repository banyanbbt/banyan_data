from django.db import models
from jsonfield import JSONField
from apps.question.model_status import question_status, answer_status
from apps.question.question_type import question_type
from apps.util.wrapper import answer_directory_path, attachment_path
from apps.question.managers import QuestionManager, AnswerManager, AttachmentManager
from apps.user.models import UserTask


class BaseModel(models.Model):
    created = models.DateTimeField("创建时间", auto_now_add=True)
    updated = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        abstract = True


class Question(BaseModel):
    """题目"""
    code = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    task_id = models.IntegerField("所属任务id", db_index=True, null=True, blank=True)
    name = models.CharField("题目名称", max_length=255, null=True, blank=True)
    content = models.TextField("题目内容", null=True, blank=True)
    question_type = models.CharField("题目类型", choices=question_type, max_length=255, null=True, blank=True)
    has_known_answer = models.BooleanField("有已知答案", default=False)
    status = models.CharField("状态", choices=question_status, max_length=255, null=True, blank=True)

    objects = QuestionManager()

    class Meta:
        db_table = "questions"
        verbose_name = "题目"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content


class AnswerOption(BaseModel):
    """答案"""
    task_id = models.IntegerField("所属任务id", db_index=True, null=True, blank=True)
    name = models.CharField("输入项名称", max_length=255, null=True, blank=True)
    option_type = models.CharField("输入项类型", max_length=255, null=True, blank=True)
    example = models.CharField("示例内容", max_length=255, null=True, blank=True)
    is_required = models.BooleanField("输入项是否必填", default=True)
    position = models.IntegerField("输入项排序")
    status = models.CharField("状态", max_length=255, null=True, blank=True)

    class Meta:
        db_table = "answer_options"
        verbose_name = "答案选项"
        verbose_name_plural = verbose_name


class Answer(BaseModel):
    """答案"""
    user_id = models.IntegerField("用户id")
    task_id = models.IntegerField("任务id")
    question_id = models.IntegerField("题目id")
    content = JSONField("文本结果", null=True, blank=True)
    file = models.FileField("文件结果", upload_to=answer_directory_path, null=True, blank=True)
    status = models.CharField("状态", choices=answer_status, max_length=255, null=True, blank=True)
    reviewer_id = models.IntegerField("审核人id", db_index=True, null=True, blank=True)

    objects = AnswerManager()

    class Meta:
        db_table = "answers"
        verbose_name = "答案"
        verbose_name_plural = verbose_name


class Attachment(BaseModel):
    """附件"""

    task_id = models.IntegerField("任务ID", null=True, blank=True)
    question_id = models.IntegerField("题目ID", null=True, blank=True)
    detail_type = models.CharField("附件归属表类型", max_length=255, null=True, blank=True)
    detail_id = models.CharField("附件归属表ID", max_length=255, null=True, blank=True)
    file_name = models.CharField("附件名称", max_length=255, null=True, blank=True)
    file_obj = models.FileField("文件", upload_to=attachment_path, null=True, blank=True)
    created_by = models.IntegerField("创建人ID")
    status = models.CharField("审核状态(answer类型)", max_length=255, null=True, blank=True)
    reviewer_id = models.IntegerField("审核人id(answer类型)", db_index=True, null=True, blank=True)

    objects = AttachmentManager()

    class Meta:
        db_table = "attachments"
        verbose_name = "附件"
        verbose_name_plural = verbose_name


class KnownAnswer(BaseModel):
    """已知答案"""
    question_id = models.IntegerField("已知答案id", db_index=True, null=True, blank=True)
    content = JSONField("已知答案", null=True, blank=True)

    class Meta:
        db_table = "known_answer"
        verbose_name = "已知答案"
        verbose_name_plural = verbose_name
