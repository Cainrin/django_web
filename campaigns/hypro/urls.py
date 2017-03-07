# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from campaigns.hypro import views_page, views_action


urlpatterns = [
    url(r'^zh/pc.html$', views_page.zhonghangpc),
    url(r'^zh/index.html$', views_page.zhIndex),
    url(r'^zh/touch.html$', views_page.zhTouch),
    url(r'^zh/pc/index.html$', views_page.zhPcindex),
    url(r'^get_sign_package', views_action.get_sign_package),
    url(r'^ticai/index.html', views_page.ticaiIndex),
    url(r'^ticai/main.html', views_page.ticaizhuanti),
    url(r'^ticai/ticai2.html', views_page.ticai2),
    url(r'^ticai/new.html', views_page.ticainew),
    url(r'^tocloud', views_action.tocloud),
    url(r'^locta', views_page.locta),
    url(r'^zh/v2.html', views_page.zhv2),
    url(r'^zh/pcv2.html$', views_page.PCzhv2),
    url(r'^yc/getInfo', views_action.ycBlank),
    url(r'^yc/ynd.html', views_page.ynd),
    url(r'^ccy.html$', views_page.ccy),
    url(r'^yc/sendMsg$', views_action.sendMessage),
    url(r'^yc/getVerify$', views_action.getVerify),
    url(r'^yc/testynd.html$', views_page.testYnd),
    url(r'^yc/wx_ynd.html$', views_page.wxynd),
    url(r'^yc/save$', views_action.save_ynd),
    url(r'^lt_new.html$', views_page.lt_new)
]