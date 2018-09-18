from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'user'
urlpatterns = [
    url(r'^profile/$', views.UserProfilePage.as_view(), name='user-profile-page'),
    url(r'^receive/$', views.ReceiveTask.as_view(), name='user-receive'),
    url(r'^validate/$', views.SendValidateEmail.as_view(), name='user-validate'),
    url(r'^active/$', views.ActiveView.as_view(), name='user-active'),
    url(r'^withdraw/$', views.WithdrawView.as_view(), name='user-withdraw')
]
