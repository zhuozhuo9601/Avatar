from django.conf.urls import url

from fontend import views

urlpatterns = [
    url(r'^vue_text/$', views.vue_text,name='vue_text'),
    url(r'^map_bb/$', views.map_bb,name='map_bb'),
    url(r'^map_cc/$', views.map_cc,name='map_cc'),
    ]