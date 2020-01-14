from django.conf.urls import url

from fontend import views

urlpatterns = [
    url(r'^vue_text/$', views.vue_text,name='vue_text'),
    ]