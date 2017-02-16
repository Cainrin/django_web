# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from views import wxVefive
from views import sslVefive



admin.site.site_title = '南京华扬活动管理平台'
admin.site.site_header = '南京华扬活动管理平台'
admin.site.index_title = '数据管理'

admin.autodiscover()

urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    # url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',    {'document_root': 'media'}),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hypro/', include('campaigns.hypro.urls')),
    url(r'^fenda201605/', include('campaigns.fenda201605.urls')),
    url(r'^ticai/', include('campaigns.ticai.urls')),
    url(r'^testticai/', include('campaigns.ticai.urls')),
    url(r'^qiche/', include('campaigns.qiche.urls')),
    url(r'^yh/', include('campaigns.yh.urls')),
    url(r'^picc/', include('campaigns.picc.urls')),
    url(r'^qc/', include('campaigns.qc.urls')),
    url(r'^jsblank/', include('campaigns.jsblank.urls')),
    url(r'^MP_verify_q5tfBJEQpcCbYIil.txt$', wxVefive),
    url(r'^.well-known/pki-validation/fileauth.htm', sslVefive)

]
