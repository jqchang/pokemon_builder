from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.start),
    url(r'^prof$', views.prof),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^roster$', views.success),
    url(r'^logout$', views.logout),
]
