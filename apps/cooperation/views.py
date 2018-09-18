from django.http import JsonResponse
from django.views import View

from apps.cooperation.forms import DataSourceCooperationForm
from apps.user.tasks import send_feedback


class DataSourceCooperationView(View):

    def post(self, request):
        form = DataSourceCooperationForm(request.POST)
        if form.is_valid():
            form.save()
            send_feedback.delay(form.build_up_remind_email_text_content())
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
        return JsonResponse({'status': 'success', 'errors': list()})

