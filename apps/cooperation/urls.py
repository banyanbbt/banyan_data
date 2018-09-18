from django.conf.urls import url

from apps.cooperation import views

app_name = 'cooperation'
urlpatterns = [
    url(r'^$', views.DataSourceCooperationView.as_view(), name='have_data')
]
