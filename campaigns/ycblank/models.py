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
    name = models.CharField(verbose_name=u'姓名', max_length=300, null=True, blank=True)
    phone = models.CharField(verbose_name=u'手机号', max_length=300, null=True, blank=True)
    jsSyd = models.IntegerField(verbose_name=u'苏银豆', default=0)

    class Meta:
        verbose_name = u'江苏银行用户'
        verbose_name_plural = u'江苏银行用户'

    def __unicode__(self):
        return str(self.openid)


class jsPrizes(models.Model):
    user = models.ForeignKey(JsAuthor, verbose_name=u'用户')
    peasType = models.IntegerField(verbose_name=u'奖品类型', choices=FoundationConst.PEAS_CHOICES)
    Count = models.IntegerField(verbose_name=u'豆子数量')
    creatime = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = u'中奖人员名单'
        verbose_name_plural = u'中奖人员名单'

    def __unicode__(self):
        return str(self.id)


class prizePool(models.Model):
    master = models.ForeignKey(JsAuthor, verbose_name=u'主用户')
    creatime = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    unitBit = models.CharField(verbose_name=u'个位牌', null=True, blank=True, max_length=300)
    decade = models.CharField(verbose_name=u'十位牌', null=True, blank=True, max_length=300)
    hundreds = models.CharField(verbose_name=u'百位牌', null=True, blank=True, max_length=300)
    decadeOpenid = models.CharField(verbose_name=u'十位openid', null=True, blank=True, max_length=300)
    hundredOpenid = models.CharField(verbose_name=u'百位openid', null=True, blank=True, max_length=300)
    rank = models.IntegerField(verbose_name=u'轮次')
    luckChance = models.CharField(verbose_name=u'命中数', max_length=300)
    hasFinished = models.BooleanField(verbose_name=FoundationConst.VN_HAS_FINISHED, default=False)

    class Meta:
        verbose_name = u'作品明晰'
        verbose_name_plural = u'作品明晰'

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

