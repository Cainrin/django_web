# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from campaigns.hypro import views_page, views_action


urlpatterns = [
    url(r'^zh/index.html$', views_page.zhIndex),
    url(r'^zh/touch.html$', views_page.zhTouch),
    url(r'^zh/pc/index.html$', views_page.zhPcindex),
    url(r'^get_sign_package', views_action.get_sign_package),
    url(r'^ticai/index.html', views_page.ticaiIndex),
    url(r'^ticai/main.html', views_page.ticaizhuanti),
    url(r'^ticai/new.html', views_page.ticainew),
    url(r'^tocloud', views_action.tocloud),
    url(r'^getlocation', views_action.getLocation),
    url(r'^locta', views_page.locta)
]