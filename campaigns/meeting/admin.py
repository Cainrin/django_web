# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .const import WorkConst
from campaigns.foundation.const import FoundationConst
from .models import WXUser, PageView, UniqueVisitor, met_hitprice, met_Author, met_Message
from .applet import cheat
from campaigns.foundation.actions import action_export_excel, form_platform_validate



class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image_tag', 'phoneNum']
    search_fields = ['phoneNum']
    actions = [action_export_excel(), ]


    def image_tag(self, obj):
        return format_html(FoundationConst.TAG_LIST_DISPLAY_IMAGE, obj.headimg)
    image_tag.short_description = WorkConst.SD_IMAGE_TAG

class MsgAdmin(admin.ModelAdmin):
    list_display = ['id']


class hitprize(admin.ModelAdmin):
    list_display = ['id']


admin.site.register(met_Author, AuthorAdmin)
admin.site.register(met_Message, MsgAdmin)
admin.site.register(met_hitprice, hitprize)