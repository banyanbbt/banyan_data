import json

from django.shortcuts import render, get_object_or_404, render_to_response
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from apps.home.forms import LoginForm, RegisterForm
from apps.customer.forms import CustomerRegisterForm
from apps.user.models import UserProfile, Feedback, UserTask, UserValidateCode, UserApplyInterfaceInfo
from apps.task.models import Task
from apps.customer.models import Customer
from apps.question.models import Attachment, AnswerOption
from apps.question.model_status import ATTACHMENT_TYPE
from apps.util.wrapper import login, logout, current_user, get_session, get_refer, set_session
from apps.util.reward_action import BanyanRewardRules, BanyanSender
from apps.user.tasks import send_verify_email, send_feedback
from apps.util.sms import content_template, apply_interface_template, corporate_account_application


@csrf_exempt
def page_not_found(request):
    """404"""
    return render_to_response('home/404.html')


class NotFoundView(View):
    def get(self, request):
        return render(request, 'home/404.html')


class HomePage(View):

    def get(self, request):
        return render(request, 'home/index.html')


class DaZhong(View):

    def get(self, request):
        return render(request, 'home/index_vw_detail.html')


class MtcTags(View):

    def get(self, request):
        return render(request, 'home/index_frog_detail.html')


class Mego(View):

    def get(self, request):
        return render(request, 'home/index_mego_detail.html')


class Finance(View):

    def get(self, request):
        return render(request, 'home/index_finance_detail.html')


class Luxury(View):

    def get(self, request):
        return render(request, 'home/index_luxury_detail.html')


class InterfacesView(View):

    def get(self, request):
        return render(request, 'home/interfaces.html')


class HaveData(View):

    def get(self, request):
        return render(request, 'home/have_data.html')


class InterfacesDetailView(View):

    def get(self, request, pk):
        template_file = "home/interfaces_detail" + str(pk) + ".html"
        return render(request, template_file)


class TasksPage(View):

    def get(self, request):
        tasks = Task.objects.filter(end_time__gte=now()).order_by('start_time')
        now_time = now()
        user = current_user(request)
        if user:
            user_task_ids = UserTask.objects.filter(user_id=user.id).values_list('task_id', flat=True)
        else:
            user_task_ids = list()
        return render(request, 'home/tasks.html', {'tasks': tasks,
                                                   'user_task_ids': user_task_ids,
                                                   'user': user,
                                                   'now_time': now_time})


class TasksDetailPage(View):

    def get(self, request, pk):
        now_time = now()
        user = current_user(request)
        task = get_object_or_404(Task.objects.all(), pk=pk)
        if user:
            user_task_ids = UserTask.objects.filter(user_id=user.id).values_list('task_id', flat=True)
        else:
            user_task_ids = list()
        # attachment
        attach = Attachment.objects.filter(detail_type=ATTACHMENT_TYPE['task'], detail_id=task.id).first()

        # 数据样例
        if AnswerOption.objects.filter(task_id=task.id).exists():
            answer_option = AnswerOption.objects.filter(task_id=task.id).order_by('position')
        else:
            answer_option = ''
        return render(request, 'home/tasks_detail.html', {'task': task, 'attach': attach,
                                                          'user_task_ids': user_task_ids,
                                                          'now_time': now_time, 'user': user,
                                                          'answer_option': answer_option})


class ProductsPage(View):

    def get(self, request):
        return render(request, 'home/products.html')


class CooperationPage(View):

    def get(self, request):
        return render(request, 'home/cooperation.html')


class ContactsPage(View):

    def get(self, request):
        return render(request, 'home/contacts.html')


class UserAuthView(View):

    def get(self, request):
        if current_user(request):
            return HttpResponseRedirect(reverse("home:home-page"))
        login_form = LoginForm()
        register_form = RegisterForm()
        error = {}
        if request.GET.get('action'):
            flag = False
        else:
            flag = True
        if request.GET.get('ea'):
            ea = True
        else:
            ea = False
        if request.GET.get('code', ''):
            code = True
        else:
            code = False
        # get referer
        pre_url = get_refer(request)
        if pre_url:
            set_session(request, 'pre_url', pre_url)
        return render(request, 'home/auth.html', {'login_form': login_form,
                                                  'reg_form': register_form,
                                                  'flag': flag,
                                                  'ea': ea,
                                                  'code': code,
                                                  'log_error': error,
                                                  'reg_error': error})


class UserRegisterView(View):

    def post(self, request):
        if request.POST.get('regist_account', '') == 'regist_company_account':
            crf = CustomerRegisterForm(request.POST)
            if crf.is_valid():
                contact_name = crf.cleaned_data.get('company_people')
                company_name = crf.cleaned_data.get('company_name')
                contact_mobile = crf.cleaned_data.get('company_tele')
                Customer.objects.create_init_customer(contact_name=contact_name,
                                                      company_name=company_name,
                                                      contact_mobile=contact_mobile)
                send_feedback.delay(corporate_account_application.format(company_name, contact_name, contact_mobile))
                return HttpResponseRedirect('/auth/?action=1&code=200/')
            else:
                customer_error = crf.errors
                login_form = LoginForm()
                register_form = RegisterForm()
                return render(request, 'home/auth.html', {'login_form': login_form,
                                                          'reg_form': register_form,
                                                          'customer_error':  customer_error,
                                                          'ea': True,
                                                          'flag': False})

        else:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                email = register_form.cleaned_data['email']
                password = register_form.cleaned_data['password']
                user = UserProfile.objects.create_user(email=email,
                                                       password=password)
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
                BanyanSender.send_reward(user_id=user.id, rule=BanyanRewardRules.REGISTER)
                return HttpResponseRedirect(reverse("home:auth"))
            else:
                error = register_form.errors
                login_form = LoginForm()
                register_form = RegisterForm()
                return render(request, 'home/auth.html', {'login_form': login_form,
                                                          'reg_form': register_form,
                                                          'reg_error': error,
                                                          'flag': False})


class UserLoginView(View):

    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            user = UserProfile.objects.filter(email=email).first()
            login(request, user)
            if user and user.is_company():
                return HttpResponseRedirect(reverse("billing:billing-home-page"))
            else:
                pre_url = get_session(request, 'pre_url')
                if pre_url:
                    return HttpResponseRedirect(pre_url)
                return HttpResponseRedirect(reverse("home:home-page"))
        else:
            error = login_form.errors
            login_form = LoginForm()
            register_form = RegisterForm()
            return render(request, 'home/auth.html', {'login_form': login_form,
                                                      'reg_form': register_form,
                                                      'log_error': error,
                                                      'flag': True})


class UserLogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("home:auth"))


class FeedbackView(View):

    def post(self, request):
        # save feedback
        response_data = {'error': 0, 'message': '感谢您的反馈'}
        contact_name = request.POST.get('contact_name', '')
        company_name = request.POST.get('company_name', '')
        contact_mobile = request.POST.get('contact_mobile', '')
        contact_email = request.POST.get('contact_email', '')
        feedback_content = request.POST.get('feedback_content', '')
        params = {'contact_name': contact_name,
                  'company_name': company_name,
                  'contact_mobile': contact_mobile,
                  'contact_email': contact_email,
                  'feedback_content': feedback_content}
        Feedback.build(params)
        send_feedback.delay(content_template.format(contact_name, company_name, contact_mobile, contact_email, feedback_content))
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class ApplyInterfaceView(View):

    def post(self, request):
        product_name = request.POST.get('product_name' '')
        contact_name = request.POST.get('contact_name', '')
        contact_mobile = request.POST.get('contact_mobile', '')
        expected_dosage = request.POST.get('feedback_content', '')
        UserApplyInterfaceInfo.objects.build_apply_interface_info(product_name,
                                                                  contact_name,
                                                                  contact_mobile,
                                                                  expected_dosage)
        send_feedback.delay(apply_interface_template.format(product_name,
                                                            expected_dosage,
                                                            contact_name,
                                                            contact_mobile))
        return JsonResponse({'status': 'ok'})
