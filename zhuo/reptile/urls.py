from django.conf.urls import url

from reptile import views

urlpatterns = [
    # 每个路由信息都需要使用url函数来构造
    # url(路径, 视图)
    url(r'^reptile/$', views.reptile_index,name='reptile_index'),
    url(r'^reptile_data/$', views.reptile_data,name='reptile_data'),
]