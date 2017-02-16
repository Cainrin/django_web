# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .const import WorkConst
from campaigns.foundation.const import FoundationConst
from .models import WXUser, PageView, Work, UniqueVisitor, AdminUser, ltworkSec
from .applet import cheat
from campaigns.foundation.actions import action_export_excel, form_platform_validate



class UniqueVisitorAdmin(admin.ModelAdmin):
    list_display = ['url', 'ip', 'creationTime']
    list_filter = ['url']
    search_fields = ['creationTime']
    readonly_fields = ['creationTime', 'url', 'ip']
    actions = [action_export_excel(), ]


class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'userpasswd']
    list_filter = ['id']
    search_fields = ['id']

    def save_model(self, request, obj, form, change):
        obj.save()





class PageViewAdmin(admin.ModelAdmin):
    list_display = ['url', 'ip', 'creationTime']
    list_filter = ['url', 'creationTime']
    search_fields = ['creationTime']
    readonly_fields = ['creationTime', 'ip', 'url']
    actions = [action_export_excel(), ]



class WXUserAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'city', 'gender', 'status', 'creationTime']
    list_filter = ['status', 'creationTime']
    search_fields = ['uuid', 'nickname']
    readonly_fields = ['creationTime']
    actions = [action_export_excel(), ]



class WorkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image_tag', 'creationTime', 'phone', 'city', 'district', 'addrinfo']
    list_filter = ['creationTime']
    list_editable = ['name']
    search_fields = ['creationTime']
    actions = [action_export_excel(), ]


    def image_tag(self, obj):
        return format_html(FoundationConst.TAG_LIST_DISPLAY_IMAGE, obj.imageurl)
    image_tag.short_description = WorkConst.SD_IMAGE_TAG




class ltworkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'isLT']
    list_filter = ['isLT']
    search_fields = ['phone']
    actions = [action_export_excel(), ]

admin.site.register(WXUser, WXUserAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(PageView, PageViewAdmin)
admin.site.register(UniqueVisitor, UniqueVisitorAdmin)
admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(ltworkSec, ltworkAdmin)