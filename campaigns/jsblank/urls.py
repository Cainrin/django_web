# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from campaigns.jsblank import views_page, views_action


urlpatterns = [
    url(r'^first$', views_action.checkFirst),
    url(r'^upload$', views_action.uploadInfo),
    url(r'^prizdraw$', views_action.chance),
    url(r'^rank$', views_action.checkRank),
    url(r'^self$', views_action.getPeas),
    url(r'^get_sign_package', views_action.get_sign_package),
    url(r"^cacheset$", views_action.setCache),
    url(r'^chanceset$', views_action.setChance),
    url(r'^index.html$', views_page.index),
    url(r'^lbsBack$', views_page.lbs_back),
    url(r'^ccy.html$', views_page.lbs_ccy),
    url(r'^share.html$', views_page.share),
    url(r'^openid', views_action.prinTopenid),
    url(r'^shadowPoint$', views_action.shadowPoint)
]