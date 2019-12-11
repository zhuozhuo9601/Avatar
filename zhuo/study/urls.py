from django.conf.urls import url

from study import views

urlpatterns = [
    url(r'^study_first/$', views.study_first,name='study_first'),
    url(r'^study_send/$', views.send,name='send'),
    url(r'^study_text/$', views.study_text,name='study_text'),
    url(r'^study_json/$', views.study_json,name='study_json'),
    url(r'^forget/$', views.forget,name='forget'),
    url(r'^forget_email/$', views.forget_email,name='forget_email'),
    url(r'^forget_password/$', views.forget_password,name='forget_password'),
    url(r'^forget_modify/$', views.forget_modify,name='forget_modify'),
    url(r'^community/$', views.community,name='community'),
    url(r'^comment/$', views.comment,name='comment'),
    url(r'^comm_store/$', views.comm_store,name='comm_store'),
    # url(r'^study_first/(?P<id>\d+)/$', views.study_first,name='study_first'),
]