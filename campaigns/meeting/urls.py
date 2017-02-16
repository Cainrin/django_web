# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from campaigns.meeting import views_page, views_action


urlpatterns = [
    url(r'^blind$', views_action.infoCache),
    url(r'^getmsg$', views_action.readMsg),
    url(r'^sendmsg$', views_action.sendMsg),
    url(r'^prizeDraw', views_action.hitPrize),
    url(r'^save$', views_action.saveTcload),
    url(r'^check$', views_action.checkBlind),
    url(r'^index', views_page.index),
    url(r'^pc$', views_page.pc),
    url(r'^draw.html$', views_page.draw)
]