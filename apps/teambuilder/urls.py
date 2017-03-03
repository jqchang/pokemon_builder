from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="teambuilder"),
    url(r'^stat_ajax/?$', views.stat_ajax),
    url(r'^battle$', views.battle),
    url(r'^battle_ajax$', views.battle_ajax)
]
