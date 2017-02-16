# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from campaigns.ycblank import views_page, views_action


urlpatterns = [
    url(r'^unit$', views_action.unit),
    url(r'^upload$', views_action.uploadInfo),
    url(r'^prizdraw$', views_action.chance),
    url(r'^shareOther$', views_action.shareOther),
    url(r'^getFinish$', views_action.getFinish),
    url(r'^get_sign_package', views_action.get_sign_package),
    url(r'^index.html$', views_page.index),
    url(r'^checkSelf$', views_action.checkSelf),
    url(r'^setChace$', views_action.getChace),
    url(r'^nickname$', views_action.nickName),
    url(r'^error.html$', views_page.lbs_back)

]