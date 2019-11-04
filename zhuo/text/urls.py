from django.conf.urls import url
from django.conf.urls.static import static

from text import views
from zhuo import settings

urlpatterns = [
    # 每个路由信息都需要使用url函数来构造
    # url(路径, 视图)
    url(r'^register/$', views.RegisterView.as_view(),name='register'),
    url(r'^login/$', views.LoginView.as_view(),name='login'),
    url(r'^index/$', views.IndexView.as_view(),name='index'),
    url(r'^user/$', views.UserView.as_view(),name='user'),
    url(r'^image/$', views.ImageView.as_view(),name='image'),
]