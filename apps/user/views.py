import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.utils.crypto import get_random_string
from django.db import transaction

from apps.user.models import UserReward, UserTask, UserValidateCode, UserProfile, UserWithdraw
from apps.task.models import Task
from apps.util.decorate import login_required
from apps.util.wrapper import current_user
from apps.user.model_status import USER_TASK_STATUS
from apps.user.tasks import send_verify_email
from apps.user.functions import validate_withdraw
from apps.util.reward_action import BanyanRewardRules, BanyanSender


logger = logging.getLogger('django')


class UserProfilePage(View):

    @method_decorator(login_required)
    def get(self, request):
        user = current_user(request)
        email = user.email
        bbn_balance = user.bbn_count
        rewards = UserReward.objects.filter(user_id=user.id)
        return render(request, 'user/profile.html', {"user": user,
                                                     "email": email,
                                                     'is_valid_email': user.is_valid_email,
                                                     "bbn_balance": bbn_balance,
                                                     "rewards": rewards})


class SendValidateEmail(View):

    @method_decorator(login_required)
    def get(self, request):
        """发送邮箱验证"""
        user = current_user(request)
        email = request.GET.get('email', '')
        if not email or not user:
            return render(request, 'user/missing_param.html')
        captcha = UserValidateCode.objects.filter(user_id=user.id, email=email, is_used=False).first()
        if captcha:
            code = captcha.code
        else:
            code = get_random_string(8)
            UserValidateCode.objects.get_or_create(user_id=user.id,
                                                   email=email,
                                                   code=code,
                                                   is_used=False,
                                                   defaults={'user_id': user.id,
                                                             'email': email,
                                                             'code': code,
                                                             'is_used': False})
        send_verify_email.delay(email, code, user.id)
        return JsonResponse({'status': 'ok'})


class ActiveView(View):

    def get(self, request):
        """验证邮箱"""
        code = request.GET.get('code', '')
        user_id = request.GET.get('u', '')
        if code and user_id:
            validate_code = UserValidateCode.objects.filter(user_id=user_id, code=code, is_used=False).first()
            if validate_code:
                user = UserProfile.objects.filter(pk=user_id).first()
                if user and not user.is_valid_email:
                    user.is_valid_email = True
                    user.save()
                    validate_code.is_used = True
                    validate_code.save()
                    return render(request, 'user/validate_success.html')
        return render(request, 'home/404.html')


class ReceiveTask(View):
    """领取任务"""

    @method_decorator(login_required)
    def post(self, request):
        user = current_user(request)
        if user:
            task_id = request.POST.get('task_id', '')
            res = dict()
            res['msg'] = "领取失败,请稍后再试"
            if user and task_id:
                task = Task.objects.filter(pk=int(task_id),
                                           start_time__lte=now(),
                                           end_time__gte=now()).first()
                if task:
                    submit_task = {'user_id': user.id,
                                   'task_id': task_id,
                                   'status': USER_TASK_STATUS[0][0],
                                   'is_file_answer': task.is_file_answer}
                    if UserTask.objects.filter(user_id=user.id, task_id=task_id).exists():
                        res['msg'] = "您已经领取过该任务了, 请勿重复领取"
                    else:
                        UserTask.objects.create(**submit_task)
                        task.received_count += 1
                        task.save()
                        res['msg'] = "领取成功"
                else:
                    res['msg'] = "非任务有效时段, 无法领取"
            else:
                res['msg'] = "领取失败,请稍后再试"
            return JsonResponse(res)


class WithdrawView(View):
    """用户提现"""

    @method_decorator(login_required)
    def post(self, request):

        user = current_user(request)
        wallet_address = request.POST.get("wallet_address", "")
        bbn_count = int(request.POST.get("bbn_count") or 0)
        error = validate_withdraw(user.id, bbn_count, wallet_address)
        if error:
            if error['count_error'] or error['address_error']:
                return JsonResponse(error)
        else:

            try:
                with transaction.atomic():
                    BanyanSender.send_reward(user_id=user.id,
                                             rule=BanyanRewardRules.withdraw_rule(bbn_count))

                    UserWithdraw.objects.create(user_id=user.id,
                                                bbn_count=bbn_count,
                                                wallet_address=wallet_address,
                                                status="未打币")
            except Exception as e:
                logger.error(e)
                return JsonResponse({"address_error": "暂时无法提现, 请稍后再试"})

        return JsonResponse({"msg": "提现成功"})


