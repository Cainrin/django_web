# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .const import WorkConst
from campaigns.foundation.const import FoundationConst
from .models import WXUser, PageView, UniqueVisitor, JsAuthor, prizePool, peasCount, ExcelMode
from .applet import cheat, DrawExcel
from campaigns.foundation.actions import action_export_excel, form_platform_validate


class UniqueVisitorAdmin(admin.ModelAdmin):
    list_display = ['url', 'ip', 'creationTime']
    list_filter = ['url']
    search_fields = ['creationTime']
    readonly_fields = ['creationTime', 'url', 'ip']
    actions = [action_export_excel(), ]




class PageViewAdmin(admin.ModelAdmin):
    list_display = ['url', 'ip', 'creationTime']
    list_filter = ['url', 'creationTime']
    search_fields = ['creationTime']
    readonly_fields = ['creationTime', 'ip', 'url']
    actions = [action_export_excel(), ]



class JsAuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', 'phone', 'jsSyd', 'name']
    search_fields = ['name', 'phone']
    actions = [action_export_excel()]


class prizePoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'creatime', 'location']
    search_fields = ['creatime']
    list_filter = ['location', 'peasType', 'user']
    actions = [action_export_excel()]



class peasCountAdmin(admin.ModelAdmin):
    list_display = ['id', 'peasType', 'Count', 'peaSend']
    search_fields = ['id']
    list_filter = ['peasType']



class ExcelAdmin(admin.ModelAdmin):
    list_display = ['comment', 'hasFinished', 'creationTime', 'updateTime', 'excelUrl']
    search_fields = ['comment']
    readonly_fields = ['creationTime', 'updateTime', 'hasFinished']
    actions = [action_export_excel(), ]

    def save_model(self, request, obj, form, change):
        vcp = DrawExcel.DrawExcelProcess(obj)
        vcp.start()


admin.site.register(PageView, PageViewAdmin)
admin.site.register(UniqueVisitor, UniqueVisitorAdmin)
admin.site.register(JsAuthor, JsAuthorAdmin)
admin.site.register(prizePool, prizePoolAdmin)
admin.site.register(peasCount, peasCountAdmin)
admin.site.register(ExcelMode, ExcelAdmin)