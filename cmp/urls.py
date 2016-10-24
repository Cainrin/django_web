# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from campaigns.picc.views_page import errorpage

admin.site.site_title = '南京华扬活动管理平台'
admin.site.site_header = '南京华扬活动管理平台'
admin.site.index_title = '数据管理'

admin.autodiscover()
handler404 = errorpage
handler500 = errorpage

urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    # url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',    {'document_root': 'media'}),
    url(r'^guess/', include('campaigns.nihuawocai.urls')),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^lottery/', include('campaigns.lottery.urls')),
    url(r'^management/', include('campaigns.management.urls')),
    url(r'^testproject/', include('campaigns.testproject.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fenda201605/', include('campaigns.fenda201605.urls')),
    url(r'^yiquan/', include('campaigns.yiquan.urls')),
    url(r'^testticai/', include('campaigns.testticai.urls')),
    url(r'^testticai/', include('campaigns.testticai.urls')),
    url(r'^qiche/', include('campaigns.qiche.urls')),
    url(r'^yh/', include('campaigns.yh.urls')),
    url(r'^picc/', include('campaigns.picc.urls'))

]
