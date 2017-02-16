# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .const import WorkConst
from campaigns.foundation.const import FoundationConst
from .models import WXUser, Author, Work, Share, Vote, VoteCheat, PageView, UniqueVisitor, ranDomWork
from .applet import cheat
from campaigns.foundation.actions import action_export_excel, form_platform_validate


class PageViewAdmin(admin.ModelAdmin):
    list_display = ['url', 'ip', 'creationTime']
    list_filter = ['url', 'creationTime']
    search_fields = ['url']
    readonly_fields = ['creationTime']
    actions = [action_export_excel(), ]


class UniqueVisitorAdmin(admin.ModelAdmin):
    list_display = ['url', 'ip', 'creationTime']
    list_filter = ['url']
    search_fields = ['url']
    readonly_fields = ['creationTime']
    actions = [action_export_excel(), ]


class randomDreamAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'id', 'rank']
    search_fields = ['rank']
    list_editable = ['rank']

    def image_tag(self, obj):
        return format_html(FoundationConst.TAG_LIST_DISPLAY_IMAGE, obj.imageurl)
    image_tag.short_description = WorkConst.SD_IMAGE_TAG



class wxUserAdmin(admin.ModelAdmin):
    list_display = ['openid', 'nickname', 'creationTime']
    list_filter = ['id']
    search_fields = ['id']
    readonly_fields = []
    actions = [action_export_excel(), ]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'cellphone', 'creationTime', 'comment']
    search_fields = ['id']
    actions = [action_export_excel(), ]


class WorkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'string', 'image_tag', 'author', 'type', 'votedCount', 'status']
    search_fields = ['id']
    list_filter = ['creationTime']
    actions = [action_export_excel()]


    def image_tag(self, obj):
        return format_html(FoundationConst.TAG_LIST_DISPLAY_IMAGE, obj.imageurl)
    image_tag.short_description = WorkConst.SD_IMAGE_TAG


class VoteCheatAdmin(admin.ModelAdmin):
    list_display = ['comment', 'type', 'minute', 'totalCount', 'nowCount', 'hasFinished', 'creationTime', 'updateTime']
    list_filter = ['type']
    search_fields = ['comment']
    readonly_fields = ['creationTime', 'updateTime', 'hasFinished']
    actions = [action_export_excel(), ]

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.nowCount == 0:
            vcp = cheat.VoteCheatProcess(obj)
            vcp.start()



admin.site.register(WXUser, wxUserAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(PageView, PageViewAdmin)
admin.site.register(UniqueVisitor, UniqueVisitorAdmin)
admin.site.register(VoteCheat, VoteCheatAdmin)
admin.site.register(ranDomWork, randomDreamAdmin)