import logging
from config.celery_configs import app
from lib.sms import client as sms_client
from lib.blockchain.pandora import Pandora
from apps.user.models import UserProfile

logger = logging.getLogger(__name__)


@app.task
def sync_monthly_billing():
    logger.info("start sync_monthly_billing")
    accounts = UserProfile.company_accounts()
    for account in accounts:
        Pandora.monthly_bill(account)
    logger.info("end sync_monthly_billing")


@app.task
def sync_weekly_billing():
    logger.info("start sync_weekly_billing")
    accounts = UserProfile.company_accounts()
    for account in accounts:
        Pandora.weekly_bill(account)
    logger.info("end sync_weekly_billing")




