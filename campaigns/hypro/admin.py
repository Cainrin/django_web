# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .const import WorkConst
from campaigns.foundation.const import FoundationConst
from .models import WXUser, PageView, UniqueVisitor, ycBlank, ycBank2, msgCode
from .applet import cheat
from campaigns.foundation.actions import action_export_excel, form_platform_validate


class msgCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'creatime', 'verifyCode', 'phone']

class ycBlankAdmin(admin.ModelAdmin):
    list_display = ['name', 'phoneNum', 'location', 'Tcreatime']
    search_fields = ['Dcreatime']
    list_filter = ['Dcreatime']
    actions = [action_export_excel()]


class UniqueVisitorAdmin(admin.ModelAdmin):
    list_display = ['url', 'ip', 'creationTime']
    list_filter = ['url']
    search_fields = ['url']
    readonly_fields = ['creationTime']
    actions = [action_export_excel(), ]

class ycBlank2Admin(admin.ModelAdmin):
    list_display = ['name', 'phoneNum', 'location', 'Tcreatime', 'isVerify']
    search_fields = ['Dcreatime']
    list_filter = ['Dcreatime']
    actions = [action_export_excel()]





class PageViewAdmin(admin.ModelAdmin):
    list_display = ['url', 'ip', 'creationTime']
    list_filter = ['url', 'creationTime']
    search_fields = ['url']
    readonly_fields = ['creationTime']
    actions = [action_export_excel(), ]



admin.site.register(ycBlank, ycBlankAdmin)
admin.site.register(PageView, PageViewAdmin)
admin.site.register(ycBank2, ycBlank2Admin)
admin.site.register(UniqueVisitor, UniqueVisitorAdmin)
admin.site.register(msgCode, msgCodeAdmin)