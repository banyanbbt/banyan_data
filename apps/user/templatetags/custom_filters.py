from django import template
from django.utils.timezone import now
from apps.question.models import Question, Answer, Attachment
from apps.task.models import Task
from apps.question.model_status import question_status
register = template.Library()


@register.filter
def symbol(value):
    """收支符号"""
    if int(value) > 0:
        return "+" + str(value)
    else:
        return str(value)


@register.filter
def question_count(value):
    """题目总量"""
    return Question.objects.filter(task_id=value).count()


@register.filter
def remain_count(value):
    """剩余待解决题目数量"""
    return Question.objects.filter(task_id=value,
                                   status=question_status[0][0]).count()


@register.filter
def get_task_remain_people(value):
    task = Task.objects.filter(pk=value).first()
    return task.max_count - task.received_count


@register.filter
def get_task_name_by_id(value):
    """根据任务id获取任务名称"""
    return Task.objects.filter(pk=value).first().name


@register.filter
def get_task_type_by_id(value):
    """根据任务id获取任务类型"""
    return Task.objects.filter(pk=value).first().type


@register.filter
def get_question_price_by_id(value):
    """根据任务id获取任务类型"""
    return Task.objects.filter(pk=value).first().question_price


@register.filter
def get_attachment_id_by_id(value):
    """根据任务id获取任务附件id"""
    return Task.objects.filter(pk=value).first().attachment_id


@register.filter
def get_answer_type_by_id(value):
    """根据任务id获取任务答案类型(是否需要上传文件)"""
    return Task.objects.filter(pk=value).first().is_file_answer


@register.filter
def get_transaction_question_code_by_id(value):
    """根据任务id获取题目id"""
    return Question.objects.filter(task_id=value, question_type="文件翻译", status="unresolved").first().code


@register.filter
def get_cleaning_question_code_by_id(value, user_id):
    """根据任务id获取清洗题目id"""
    answered_question_ids = Answer.objects.filter(user_id=user_id, task_id=value).exclude(status="审核未通过").values_list('question_id', flat=True)
    return Question.objects.get_random_question(task_id=value, answered_question_ids=answered_question_ids).code


@register.filter
def get_upload_img_question_code_by_id(value):
    """根据任务id获取图片上传题目id"""
    return Question.objects.filter(task_id=value, question_type="图片上传", status="unresolved").first().code


@register.filter
def en_to_cn(value):
    """将英文字段转换为中文"""
    if value == "car_brand":
        return "车品牌"
    if value == "car_serie":
        return "车系"
    if value == "car_type":
        return "车型"
    if value == "car_version":
        return "版本"
    if value == "car_gearbox":
        return "变速箱"
    if value == "engine_capacity":
        return "排量"
    if value == "car_price":
        return "价格"
    if value == "car_level":
        return "级别"
    if value == "enterprises_name":
        return "企业工商名称"
    if value == "social_credit_code":
        return "企业工商统一社会信用代码"
    if value == "app_name":
        return "APP名称"


@register.filter
def is_img_upload_task(value):
    task = Task.objects.get(pk=value)
    return task.type == '图片'


@register.filter
def transfer_task_type(value):
    if value == "包装食品营养成分图搜集":
        return "食品"
    if value == "药品二维码图片搜集":
        return "药品"
    if value == "国内景区图片采集":
        return "景区"


@register.filter
def get_finish_count(value):
    """根据任务id获取图片上传任务的完成数量"""
    question_ids = Attachment.objects.filter(task_id=value.task_id, created_by=value.user_id).values_list('question_id',
                                                                                                          flat=True)
    return len(set(question_ids))


@register.filter
def has_remain_question(value):
    """判断该任务下的题目是否已经做完"""
    answered_question_ids = Attachment.objects.get_current_user_answered_question_ids(value.task_id, value.user_id)
    return Question.objects.filter(status='unresolved', task_id=value.task_id).exclude(id__in=answered_question_ids)


@register.filter
def get_received_count(value):
    """任务已领取人数"""
    if value.start_time > now():
        return 0
    else:
        return value.received_count + 50
