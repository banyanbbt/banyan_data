from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'task'
urlpatterns = [
    url(r'^$', views.TaskListPage.as_view(), name='task-list-page'),
]
