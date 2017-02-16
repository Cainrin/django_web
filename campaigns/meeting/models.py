# -*- coding: utf-8 -*-
from django.db import models
from .const import AuthorConst, WorkConst, WXUserConst, ShareConst, VoteConst, VoteCheatConst, PageViewConst, UniqueVisitorConst
from .config import WorkConfig
from campaigns.foundation.const import FoundationConst
from campaigns.foundation.applet.utils import handle_image_upload


class WXUser(models.Model):
    openid = models.CharField(max_length=200)
    nickname = models.CharField(max_length=100, null=True, blank=True, verbose_name=FoundationConst.VN_NICKNAME)
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name=FoundationConst.VN_CITY)
    gender = models.IntegerField(choices=FoundationConst.GENDER_CHOICES, verbose_name=FoundationConst.VN_GENDER)
    status = models.IntegerField(choices=FoundationConst.STATUS_CHOICES, verbose_name=FoundationConst.VN_STATUS)
    creationTime = models.DateTimeField(auto_now_add=True, verbose_name=FoundationConst.VN_CREATION_TIME)
    comment = models.CharField(max_length=100, null=True, blank=True, verbose_name=FoundationConst.VN_COMMENT)

    class Meta:
        verbose_name = WXUserConst.VN_TABLE_NAME
        verbose_name_plural = WXUserConst.VN_TABLE_NAME

    def __unicode__(self):
        return self.openid




class met_hitprice(models.Model):
    openid = models.CharField(max_length=300, verbose_name=u'openid')
    hitime = models.DateTimeField(auto_now_add=True, verbose_name=u'中将时间')

    class Meta:
        verbose_name = u'中将人员'
        verbose_name_plural = u'中将人员'

    def __unicode__(self):
        return self.openid


class met_Author(models.Model):
    openid = models.CharField(null=True, blank=True, max_length=300, verbose_name=u'openid')
    headimg = models.CharField(max_length=500, verbose_name=u'头像')
    name = models.CharField(max_length=200, verbose_name=u'姓名', null=True, blank=True)
    phoneNum = models.CharField(max_length=300, verbose_name=u'电话', null=True, blank=True)

    class Meta:
        verbose_name = u'员工信息'
        verbose_name_plural = u'员工信息'

    def __unicode__(self):
        return self.name


class met_Message(models.Model):
    openid = models.CharField(max_length=300, verbose_name=u'openid')
    msg = models.CharField(max_length=500, verbose_name=u'消息')
    time = models.DateTimeField(auto_now_add=True, verbose_name=u'时间')
    isread = models.IntegerField(verbose_name=u'是否读取', choices=FoundationConst.READ_CHOICES, default=1)
    isSend = models.IntegerField(verbose_name=u'是否抽取', choices=FoundationConst.READ_CHOICES, default=1)

    class Meta:
        verbose_name = u'弹幕信息'
        verbose_name_plural = u'弹幕信息'

    def __unicode__(self):
        return self.openid






class PageView(models.Model):
    url = models.URLField(verbose_name=FoundationConst.VN_URL)
    ip = models.GenericIPAddressField(verbose_name=FoundationConst.VN_IP)
    creationTime = models.DateField(auto_now_add=True, verbose_name=FoundationConst.VN_CREATION_TIME)

    class Meta:
        verbose_name = PageViewConst.VN_TABLE_NAME
        verbose_name_plural = PageViewConst.VN_TABLE_NAME

    def __unicode__(self):
        return str(self.id)


class UniqueVisitor(models.Model):
    url = models.URLField(verbose_name=FoundationConst.VN_URL)
    wxUser = models.ForeignKey(WXUser, null=True, blank=True, verbose_name=WXUserConst.VN_TABLE_NAME)
    ip = models.GenericIPAddressField(verbose_name=FoundationConst.VN_IP)
    creationTime = models.DateField(auto_now_add=True, verbose_name=FoundationConst.VN_CREATION_TIME)

    class Meta:
        verbose_name = UniqueVisitorConst.VN_TABLE_NAME
        verbose_name_plural = UniqueVisitorConst.VN_TABLE_NAME

    def __unicode__(self):
        return str(self.id)

