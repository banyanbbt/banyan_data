from django.shortcuts import render
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.utils.timezone import now

from apps.user.models import UserTask
from apps.task.models import Task
from apps.util.decorate import login_required
from apps.util.wrapper import current_user


class TaskListPage(View):

    @method_decorator(login_required)
    def get(self, request):
        user = current_user(request)
        if user.is_company():
            tasks = Task.objects.filter(created_by=user.id)
        else:
            tasks = UserTask.objects.filter(user_id=user.id)
        return render(request, 'task/index.html', {'tasks': tasks, 'user': user, 'now_time': now()})

