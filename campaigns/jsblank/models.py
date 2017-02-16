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


class JsAuthor(models.Model):
    openid = models.CharField(verbose_name=u'openid', max_length=300)
    name = models.CharField(verbose_name=u'姓名', max_length=300)
    phone = models.CharField(verbose_name=u'手机号', max_length=300)
    jsSyd = models.IntegerField(verbose_name=u'苏银豆', default=0)

    class Meta:
        verbose_name = u'江苏银行用户'
        verbose_name_plural = u'江苏银行用户'

    def __unicode__(self):
        return self.name


class prizePool(models.Model):
    user = models.ForeignKey(JsAuthor, verbose_name=u'用户信息')
    creatime = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    location = models.CharField(verbose_name=u'位置', max_length=300)
    peasType = models.IntegerField(verbose_name=u'奖品类型', choices=FoundationConst.PEAS_CHOICES)
    peasCount = models.IntegerField(verbose_name=u'奖品数量')

    class Meta:
        verbose_name = u'中奖用户'
        verbose_name_plural = u'中奖用户'

    def __unicode__(self):
        return str(self.id)


class peasCount(models.Model):
    peasType = models.IntegerField(verbose_name=u'奖品类型', choices=FoundationConst.PEAS_CHOICES)
    Count = models.IntegerField(verbose_name=u'豆子数量')
    peaSend = models.IntegerField(verbose_name=u'发出豆子')
    max_send = models.IntegerField(verbose_name=u'每天上限发送', default=0)

    class Meta:
        verbose_name = u'奖品池'
        verbose_name_plural = u'奖品池'

    def __unicode__(self):
        return str(self.id)





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



class ExcelMode(models.Model):
    comment = models.CharField(max_length=100, verbose_name=FoundationConst.VN_COMMENT)
    choice = models.IntegerField(choices=FoundationConst.EXPORT_CHOICE)
    excelUrl = models.FileField(verbose_name=u'excel路径', null=True, blank=True)
    hasFinished = models.BooleanField(verbose_name=FoundationConst.VN_HAS_FINISHED, default=False)
    creationTime = models.DateTimeField(auto_now_add=True, verbose_name=FoundationConst.VN_CREATION_TIME)
    updateTime = models.DateTimeField(auto_now=True, verbose_name=FoundationConst.VN_UPDATE_TIME)

    class Meta:
        verbose_name = u'数据导出记录'
        verbose_name_plural = u'数据导出记录'

    def __unicode__(self):
        return self.comment