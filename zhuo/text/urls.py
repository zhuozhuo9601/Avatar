from django.conf.urls import url
from django.conf.urls.static import static

from text import views
from zhuo import settings

urlpatterns = [
    # 每个路由信息都需要使用url函数来构造
    # url(路径, 视图)
    url(r'^register/$', views.RegisterView.as_view(),name='register'),
    url(r'^login/$', views.LoginView.as_view(),name='login'),
    url(r'^$', views.IndexView.as_view(),name='index'),
    url(r'^user/$', views.UserView.as_view(),name='user'),
    url(r'^image/$', views.ImageView.as_view(),name='image'),
    url(r'^about/$', views.AboutView.as_view(),name='about'),
    url(r'^games/$', views.GamesView.as_view(),name='games'),
    url(r'^news/$', views.NewsView.as_view(),name='news'),
    url(r'^contact/$', views.ContactView.as_view(),name='contact'),
    url(r'^single/$', views.SingleView.as_view(),name='single'),
    url(r'^table/$', views.TableView.as_view(),name='table'),
    url(r'^table_add/$', views.TableAdd.as_view(),name='table_add'),
    url(r'^table_update/$', views.TableUpdate.as_view(),name='table_update'),
    url(r'^table_delete/$', views.TableDelete.as_view(),name='table_delete'),
    url(r'^echarts/$', views.EchartsView.as_view(),name='echarts'),
    url(r'^outlogin/$', views.OutLogin.as_view(),name='outlogin'),
    url(r'^user_add/$', views.UserAdd.as_view(),name='user_add'),
    url(r'^user_city/$', views.UserProvince,name='user_city'),
    url(r'^gui_password/$', views.gui_password,name='gui_password'),
    url(r'^getVerificationCode/$', views.getVerificationCode,name='getVerificationCode'),
    url(r'^table_permission/$', views.table_permission,name='table_permission'),
    url(r'^check_permission/$', views.check_permission,name='check_permission'),
    url(r'^add_permission/$', views.add_permission,name='add_permission'),
]