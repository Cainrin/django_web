# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from campaigns.qc import views_page, views_action


urlpatterns = [
    url(r'^tocloud', views_action.tocloud),
    url(r'^upload', views_action.uploadPage),
    url(r'^getExcel', views_action.getExcel),
    url(r'^backadmin', views_action.backadmin),
    url(r'^Index.html$', views_page.qicheIndex)
]