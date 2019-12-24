from django.conf.urls import url

from study import views

urlpatterns = [
    url(r'^study_first/$', views.study_first,name='study_first'),
    url(r'^study_send/$', views.send,name='send'),
    url(r'^study_text/$', views.study_text,name='study_text'),
    url(r'^study_json/$', views.study_json,name='study_json'),
    url(r'^forget/$', views.forget,name='forget'),
    url(r'^forget_email/$', views.forget_email,name='forget_email'),
    url(r'^modify_password/$', views.modify_password,name='modify_password'),
    url(r'^forget_password/(?P<name>\w+)/$', views.forget_password,name='forget_password'),
    url(r'^set_password/$', views.set_password,name='set_password'),
    url(r'^update_password/$', views.update_password,name='update_password'),
    url(r'^community/$', views.community,name='community'),
    url(r'^comment/$', views.comment,name='comment'),
    # url(r'^comment/(?P<page>\d+)/(?P<ids>\d+)/$', views.comment,name='comment'),
    url(r'^comm_store/$', views.comm_store,name='comm_store'),
    url(r'^comm_like/$', views.comm_like,name='comm_like'),
    url(r'^error_404/$', views.error_404,name='error_404'),
    # url(r'^study_first/(?P<id>\d+)/$', views.study_first,name='study_first'),
]