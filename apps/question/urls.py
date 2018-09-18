from django.conf.urls import url
from apps.question.views import QuestionView, file_upload, ImgUploadView

app_name = 'question'
urlpatterns = [
    url(r'^upload/$', file_upload, name='file-upload'),
    url(r'^img_upload/$', ImgUploadView.as_view(), name='img-upload'),
    url(r'^(?P<pk>\w+)/$', QuestionView.as_view(), name='get-question'),
]
