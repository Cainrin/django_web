# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .const import WorkConst
from campaigns.foundation.const import FoundationConst
from .models import WXUser, CountPUV, AdminLog, AdminUser, WXUser, UsrPhoneCall, walkCount, qrcount, hitprize, weekCount, addCode, PageView
from .applet import cheat
from campaigns.foundation.actions import action_export_excel, form_platform_validate



class weekCountAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid']



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
    list_display = ['walk', 'money', 'change', 'creaTime', 'openid']
    search_fields = ['id']


class WXuserAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid']
    list_filter = ['creationTime']

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


class qrcountAdmin(admin.ModelAdmin):
    list_display = ['id']
    search_fields = ['code']


class hitprizeAdmin(admin.ModelAdmin):
    list_display = ['id']


class PhoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'openid', "usractive", "signuptime", "usrsignup", "prizetime", "usrprizes"]
    list_filter = ['id']


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