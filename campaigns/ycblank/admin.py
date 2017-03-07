# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .const import WorkConst
from campaigns.foundation.const import FoundationConst
from .models import WXUser, PageView, UniqueVisitor, JsAuthor, prizePool, peasCount, jsPrizes
from .applet import cheat
from campaigns.foundation.actions import action_export_excel, form_platform_validate



class WXUserAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'city', 'gender', 'status', 'creationTime']
    list_filter = ['status', 'creationTime']
    search_fields = ['openid', 'nickname']
    readonly_fields = ['creationTime']
    actions = [action_export_excel(), ]






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


class jsPrizesAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'peasType', 'Count', 'creatime']
    search_fields = ['user']
    list_filter = ['peasType']
    actions = [action_export_excel()]




class JsAuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', 'phone', 'jsSyd']
    search_fields = ['openid']
    actions = [action_export_excel()]

#
class prizePoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'master', 'hasFinished', 'luckChance', 'creatime']
    search_fields = ['master__openid']
    actions = [action_export_excel()]



class peasCountAdmin(admin.ModelAdmin):
    list_display = ['id', 'peasType', 'Count', 'peaSend']
    search_fields = ['id']
    list_filter = ['peasType']
    actions = [action_export_excel()]


admin.site.register(PageView, PageViewAdmin)
admin.site.register(UniqueVisitor, UniqueVisitorAdmin)
admin.site.register(JsAuthor, JsAuthorAdmin)
admin.site.register(prizePool, prizePoolAdmin)
admin.site.register(jsPrizes, jsPrizesAdmin)
admin.site.register(peasCount, peasCountAdmin)
admin.site.register(WXUser, WXUserAdmin)