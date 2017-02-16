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


class AdminUser(models.Model):
    username = models.CharField(verbose_name=u"管理员昵称", max_length=100)
    userpasswd = models.CharField(verbose_name=u"密码", max_length=100)

    class Meta:
        verbose_name = u"后台管理员账户"
        verbose_name_plural = u"后台管理员账户"

    def __unicode__(self):
        return str(self.username)




class Work(models.Model):
    name = models.CharField(max_length=300, verbose_name=FoundationConst.VN_NAME)
    phone = models.CharField(max_length=300, verbose_name=FoundationConst.VN_STRING)
    imageurl = models.ImageField(upload_to="", verbose_name=FoundationConst.VN_IMAGE, max_length=399)
    creationTime = models.DateTimeField(auto_now_add=True, verbose_name=FoundationConst.VN_CREATION_TIME)
    city = models.CharField(max_length=300, verbose_name=u'某市')
    district = models.CharField(max_length=300, verbose_name=u'区/县')
    addrinfo = models.CharField(max_length=300, verbose_name=u'详细地址')
    network = models.CharField(max_length=300, verbose_name=u'网络信息')
    status = models.IntegerField(choices=FoundationConst.STATUS_CHOICES, verbose_name=u'状态', default=10)

    class Meta:
        verbose_name = WorkConst.VN_TABLE_NAME
        verbose_name_plural = WorkConst.VN_TABLE_NAME

    def __unicode__(self):
        return ""


class ltworkSec(models.Model):
    name = models.CharField(max_length=300, verbose_name=FoundationConst.VN_NAME)
    phone = models.CharField(max_length=300, verbose_name=FoundationConst.VN_STRING)
    isLT = models.IntegerField(verbose_name=u'是否是联通', choices=FoundationConst.LT_CHOICE)

    class Meta:
        verbose_name_plural = u'联通二期'
        verbose_name = u'联通二期'

    def __unicode__(self):
        return self.name




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



class usrInfo(models.Model):
    name = models.CharField(max_length=300, verbose_name=u'姓名')
    phone = models.CharField(max_length=300, verbose_name=u'电话')
    creatime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'用户信息表'
        verbose_name_plural = u'用户信息表'

    def __unicode__(self):
        return self.name