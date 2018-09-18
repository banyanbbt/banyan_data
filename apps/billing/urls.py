from django.urls import path
from django.conf.urls import url
from apps.billing.views import BillingHome, AccountBillDataView

from . import views

app_name = 'billing'
urlpatterns = [
    url(r'^$', BillingHome.as_view(), name='billing-home-page'),
    url(r'^data_list/$', AccountBillDataView.as_view(), name='billing-data-page'),
]
