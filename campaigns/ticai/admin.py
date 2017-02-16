# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .const import WorkConst
from campaigns.foundation.const import FoundationConst
from .models import WXUser, CountPUV, AdminLog, AdminUser, WXUser, UsrPhoneCall, walkCount, qrcount, hitprize, weekCount, addCode, PageView, VoteCheat, ExcelMode
from .applet import sendPrice, DrawExcel
from campaigns.foundation.actions import action_export_excel, form_platform_validate



class weekCountAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid']
    search_fields = ['openid']



class CountPUVAdmin(admin.ModelAdmin):
    list_display = ['pv', 'uv', 'addpv', 'adduv']
    list_filter = ['id']
    search_fields = ['id']
    readonly_fields = []
    actions = [action_export_excel(), ]

    def save_model(self, request, obj, form, change):
        obj.save()

class testAdmin(admin.ModelAdmin):
    list_display = ['id']

class pvAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_filter = ['creationTime']


class addCodeAdmin(admin.ModelAdmin):
    list_display = ['id']


class WalkAdmin(admin.ModelAdmin):
    list_display = ['id', 'walk', 'money', 'change', 'creaTime', 'openid', 'priCode']
    search_fields = ['id']
    list_filter = ['openid']



class WXuserAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', 'creationTime']
    list_filter = ['creationTime']
    search_fields = ['id']

    def save_model(self, request, obj, form, change):
        obj.save()


class AdminLogAdmin(admin.ModelAdmin):
    list_display = ['usrname', 'event', 'eventime']
    list_filter = ['eventime']
    search_fields = ['usrname']
    readonly_fields = ['event']
    actions = [action_export_excel(), ]


class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'userpasswd']
    list_filter = ['id']
    search_fields = ['id']

    def save_model(self, request, obj, form, change):
        obj.save()


class LotteryAdmin(admin.ModelAdmin):
    list_display = ['maxmon', 'prichance', 'FiChance']
    list_filter = ['id']
    search_fields = ['id']


class PriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'pricename', 'pricetype', 'pricecount', 'sendprize']
    list_filter = ['id']

    def save_model(self, request, obj, form, change):
        obj.save()

class VoteCheatAdmin(admin.ModelAdmin):
    list_display = ['comment', 'minute', 'totalCount', 'nowCount', 'hasFinished', 'creationTime', 'updateTime']
    search_fields = ['comment']
    readonly_fields = ['creationTime', 'updateTime', 'hasFinished']
    actions = [action_export_excel(), ]

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.nowCount == 0:
            vcp = sendPrice.SendPriceProcess(obj)
            vcp.start()

class ExcelAdmin(admin.ModelAdmin):
    list_display = ['comment', 'hasFinished', 'creationTime', 'updateTime']
    search_fields = ['comment']
    readonly_fields = ['creationTime', 'updateTime', 'hasFinished']
    actions = [action_export_excel(), ]

    def save_model(self, request, obj, form, change):
        obj.save()
        vcp = DrawExcel.DrawExcelProcess(obj)
        vcp.start()

class qrcountAdmin(admin.ModelAdmin):
    list_display = ['id']
    search_fields = ['id']



class hitprizeAdmin(admin.ModelAdmin):
    list_display = ['id']


class PhoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', "usractive", "signuptime", "usrsignup", "prizetime", "usrprizes"]
    list_filter = ['usrprizes']


admin.site.register(CountPUV, CountPUVAdmin)
admin.site.register(AdminLog, AdminLogAdmin)
admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(WXUser, WXuserAdmin)
admin.site.register(UsrPhoneCall, PhoneAdmin)
admin.site.register(walkCount, WalkAdmin)
admin.site.register(qrcount, qrcountAdmin)
admin.site.register(hitprize, hitprizeAdmin)
admin.site.register(weekCount, weekCountAdmin)
admin.site.register(addCode, addCodeAdmin)
admin.site.register(PageView, pvAdmin)
admin.site.register(VoteCheat, VoteCheatAdmin)
admin.site.register(ExcelMode, ExcelAdmin)