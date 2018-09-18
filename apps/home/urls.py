from django.urls import path
from django.conf.urls import url
from apps.frog.views import AudienceHome

from . import views

app_name = 'home'
urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='home-page'),
    url(r'^vwimport_sharan/$', views.DaZhong.as_view(), name='dazhong-page'),
    url(r'^mtc_tags/$', AudienceHome.as_view(), name='mtc-tags'),
    url(r'^mego/$', views.Mego.as_view(), name='mego-page'),
    url(r'^finance/$', views.Finance.as_view(), name='finance-page'),
    url(r'^luxury/$', views.Luxury.as_view(), name='luxury-page'),
    url(r'^tasks/$', views.TasksPage.as_view(), name='tasks-page'),
    url(r'^tasks/(?P<pk>\d+)/$', views.TasksDetailPage.as_view(), name='tasks-detail-page'),
    url(r'^products/$', views.ProductsPage.as_view(), name='products-page'),
    url(r'^cooperation/$', views.CooperationPage.as_view(), name='cooperation-page'),
    url(r'^contacts/$', views.ContactsPage.as_view(), name='contacts-page'),
    url(r'^auth/$', views.UserAuthView.as_view(), name='auth'),
    url(r'^login/$', views.UserLoginView.as_view(), name='login-page'),
    url(r'^register/$', views.UserRegisterView.as_view(), name='register-page'),
    url(r'^logout/$', views.UserLogoutView.as_view(), name='logout'),
    url(r'^feedback/$', views.FeedbackView.as_view(), name='feedback'),
    url(r'^interfaces/$', views.InterfacesView.as_view(), name='interfaces'),
    url(r'^apply_interface/$', views.ApplyInterfaceView.as_view(), name='apply-interface'),
    url(r'^have_data/$', views.HaveData.as_view(), name='have-data'),
    url(r'^interfaces/(?P<pk>\d+)/$', views.InterfacesDetailView.as_view(), name='interfaces-detail-page'),
    # url(r'^not/$', views.NotFoundView.as_view(), name='not-found')
]
