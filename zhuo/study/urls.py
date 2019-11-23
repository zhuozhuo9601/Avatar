from django.conf.urls import url

from study import views

urlpatterns = [
    url(r'^study_first/$', views.study_first,name='study_first'),
    url(r'^study_send/$', views.send,name='send'),
    url(r'^study_text/$', views.study_text,name='study_text'),
    url(r'^study_json/$', views.study_json,name='study_json'),
    # url(r'^study_first/(?P<id>\d+)/$', views.study_first,name='study_first'),
]