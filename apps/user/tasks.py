import logging
from config.celery_configs import app
from apps.util.sms import send_validate_email, send_feedback_email_to_admin

logger = logging.getLogger(__name__)


@app.task
def send_verify_email(to, captcha, user_id):
    """发送验证邮件"""
    error = send_validate_email(to, captcha, user_id)
    if error:
        error_info = "to:{0}|user_id{1}|error:{2}".format(to, captcha, user_id)
        logger.error(error_info)
        return error_info
    else:
        return "send success"


@app.task
def send_feedback(content):
    """实时发送用户需求到admin邮箱"""
    error = send_feedback_email_to_admin(content)
    if error:
        error_info = "send feedback error:{0}".format(error)
        logger.error(error_info)
        return error_info
    else:
        return "send feedback success"
