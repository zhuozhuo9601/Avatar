from django.conf.urls import url

from study import views

urlpatterns = [
    url(r'^study_first/$', views.study_first,name='study_first'),
    # url(r'^study_first/(?P<id>\d+)/$', views.study_first,name='study_first'),
]