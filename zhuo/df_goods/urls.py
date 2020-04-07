from django.conf.urls import url

from df_goods import views

urlpatterns = [
    # 每个路由信息都需要使用url函数来构造
    # url(路径, 视图)
    url(r'^search/$', views.MySearchView(),name='haystack_search'),

]