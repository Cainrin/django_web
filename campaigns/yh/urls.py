# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from campaigns.yh import views_page, views_action


urlpatterns = [
    url(r'^upload$', views_action.upload),
    url(r'^dream', views_action.fetch_dream),
    url(r'^vote', views_action.dreamVote),
    url(r'^getSignPackage$', views_action.get_sign_package),
    url(r'^self', views_action.fetch_self),
    url(r'^usrdata', views_action.finish),
    url(r'^puv', views_action.exportExcel),
    url(r'^tocould', views_action.tocloud),
    url(r'^random$', views_action.random_dream),
    url(r'^index$', views_page.index),
    url(r'^such', views_action.such_work),
    url(r'^main.html$', views_page.Main),
    url(r'^share.html', views_page.share),
    url(r'^success.html', views_page.success),
    url(r'^upload.html$', views_page.upload),
    url(r'^fakeup', views_action.Fakeupload),
    url(r'^work.html', views_page.Work),
    url(r'^workList.html$', views_page.WorkList),
    url(r'^FakeUpload.html$', views_page.fakeUp),
    url(r'^fatchDream', views_action.fatchDream),
    url(r'^getExcel', views_action.isExcel),
    url(r'^index2.html$', views_page.index2),
    url(r'^SuchDream', views_action.suchDream),
    url(r'^addWork$', views_action.addWork),
    url(r'^randomDream$', views_action.ranDoMdream)

]
