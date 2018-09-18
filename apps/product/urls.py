from django.urls import path
from django.conf.urls import url
from apps.product.views import ProductHome, AccountProductDataView

from . import views

app_name = 'product'
urlpatterns = [
    url(r'^$', ProductHome.as_view(), name='product-home-page'),
    url(r'^data_list/$', AccountProductDataView.as_view(), name='product-data-page'),
]
