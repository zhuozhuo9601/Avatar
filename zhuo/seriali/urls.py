from django.conf.urls import url

from seriali import views

urlpatterns = [
    # url(r'^books/$', views.BookInfoViewSet.as_view({'get': 'list'})),
    url(r'^latest/$', views.BookInfoViewSet.as_view({'get': 'latest'})),
]