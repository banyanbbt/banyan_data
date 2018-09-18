import copy

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.utils.timezone import now
from apps.question.models import Question, Answer, Attachment
from apps.question.model_status import answer_status, ATTACHMENT_TYPE
from apps.question.functions import get_allow_question, get_question_return_content, get_answer_attachment_dict, \
    get_answer_dict
from apps.task.models import Task
from apps.user.models import UserTask
from apps.util.decorate import login_required
from apps.util.wrapper import current_user


class QuestionView(View):
    """题目"""

    def get(self, request, pk):
        """题目展示"""
        now_time = now()
        user = current_user(request)
        if not user:
            return HttpResponseRedirect(reverse('home:auth'))
        question = get_object_or_404(Question.objects.filter(status='unresolved'),
                                     code=pk)
        task = get_object_or_404(Task.objects.filter(start_time__lte=now_time,
                                                     end_time__gte=now_time),
                                 pk=question.task_id)
        return render(request, 'question/answer_question.html',
                      get_question_return_content(question=get_allow_question(question,
                                                                              user_id=user.id,
                                                                              task_id=task.id),
                                                  user_id=user.id,
                                                  task_id=task.id,
                                                  task_name=task.name))

    def post(self, request, pk):
        """
        提交题目
        {
            'app_name': ['cc'],
            'csrfmiddlewaretoken': ['VofYdPXeACMMojOGddXtmlRfNLbSKOzSijjcjyBF9tlzRRdN8r8c0uOLMRumvCCp'],
            'social_credit_code': ['bc'],
            'enterprises_name': ['a']
        }
        """
        user = current_user(request)
        if not user:
            return HttpResponseRedirect(reverse('home:auth'))
        question = Question.objects.get_question_by_code(code=pk)
        submit_data = copy.copy(request.POST)

        del submit_data['csrfmiddlewaretoken']

        Answer.build_answer({'user_id': user.id,
                             'task_id': question.task_id,
                             'question_id': question.id,
                             'content': submit_data})
        question = get_allow_question(question=question, user_id=user.id, task_id=question.task_id)
        return HttpResponseRedirect(reverse('question:get-question', kwargs={'pk': question.code}))


@csrf_exempt
@login_required
def file_upload(request):
    """提交文件"""
    if request.method.upper() == 'POST':
        task_id = request.POST.get('task_id', None)
        question_id = request.POST.get('question_id', None)
        user = current_user(request)
        task = Task.objects.filter(pk=task_id).first()
        file = request.FILES.get("uploadFile", None) if "uploadFile" in request.FILES else request.FILES.get("file_data", None)

        if not task_id or not question_id or not user or not file:
            return JsonResponse({'msg': "参数缺失。"})
        # 重复提交校验
        if task.is_img_task:
            if Attachment.objects.filter(task_id=task_id, question_id=question_id, created_by=user.id,
                                         detail_type=ATTACHMENT_TYPE['answer']).count() > 5:
                return JsonResponse({'msg': '该题目上传数量已达上限，请选择其他题目上传!'})
        else:
            if Answer.objects.filter(user_id=user.id,
                                     task_id=task_id,
                                     question_id=question_id,
                                     status=answer_status[0][0]).exists():
                return JsonResponse({'msg': '您已经上传过了，请耐心等待结果!'})

        answer = Answer.objects.filter(user_id=user.id, task_id=task_id, question_id=question_id).first()
        if not answer and not task.is_img_task:
            Answer.objects.create(**get_answer_dict(user, task_id, question_id))
        Attachment.objects.create(**get_answer_attachment_dict(file, user, task_id, question_id))
        if not task.is_img_task:
            UserTask.upload_success_status_for_file_answer(user.id, task_id)
        return JsonResponse({'msg': '上传成功!'})


class ImgUploadView(View):
    @method_decorator(login_required)
    def get(self, request):
        now_time = now()
        user = current_user(request)
        task_id = request.GET.get('task_id')
        if not user:
            return HttpResponseRedirect(reverse('home:auth'))
        task = get_object_or_404(Task.objects.filter(start_time__lte=now_time,
                                                     end_time__gte=now_time),
                                 pk=task_id)
        # 用于展示已完成数量
        user_task = UserTask.objects.filter(user_id=user.id, task_id=task.id).first()
        # 已经做过的题目
        answered_question_ids = Attachment.objects.get_current_user_answered_question_ids(task.id, user.id)
        obj_list = get_list_or_404(Question.objects.exclude(id__in=answered_question_ids), status='unresolved', task_id=task.id)
        return render(request, 'question/scenery_upload.html', {'obj_list': obj_list, 'task': task,
                                                                'user_task': user_task})
