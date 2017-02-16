# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .const import WorkConst
from campaigns.foundation.const import FoundationConst
from .models import WXUser, PageView, Work
from .applet import cheat
from campaigns.foundation.actions import action_export_excel, form_platform_validate



class WXUserAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'city', 'gender', 'status', 'creationTime']
    list_filter = ['status', 'creationTime']
    search_fields = ['uuid', 'nickname']
    readonly_fields = ['creationTime']
    actions = [action_export_excel(), ]



class WorkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'creationTime', 'sex', 'city', 'district', 'carType']
    list_filter = ['creationTime']
    list_editable = ['name']
    search_fields = ['id']
    actions = [action_export_excel(), ]



admin.site.register(WXUser, WXUserAdmin)
admin.site.register(Work, WorkAdmin)