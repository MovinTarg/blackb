from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.index),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^friends$', views.friends),
    url(r'^logoff$', views.logoff),
    url(r'^user/(?P<user_id>\d+)$', views.view),
    url(r'^user/(?P<user_id>\d+)/add$', views.add),
    url(r'^user/(?P<user_id>\d+)/delete$', views.delete),
]
