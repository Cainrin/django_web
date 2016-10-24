# -*- coding: utf-8 -*-
from django.utils.timezone import utc
from django.db import models
from .const import AuthorConst,PricHome, AddCode,  WorkConst, WXUserConst, ShareConst, VoteConst, VoteCheatConst, PageViewConst, UniqueVisitorConst, PricesConst, Lottery, ActiveDataConst, UserPhonecallConst
from .config import WorkConfig
from campaigns.foundation.const import FoundationConst
from campaigns.foundation.applet.utils import handle_image_upload
import datetime


class UsrPhoneCall(models.Model):
    openid = models.CharField(max_length=100, verbose_name=FoundationConst.VN_ID)
    usractive = models.CharField(verbose_name=FoundationConst.VN_USRINFO, null=True, blank=True, max_length=100, default=None)
    signuptime = models.FloatField(verbose_name=FoundationConst.VN_SIGNTIME, null=True, blank=True, default=None)
    usrsignup = models.CharField(verbose_name=FoundationConst.VN_SIGNUSR, null=True, blank=True, max_length=100, default=None)
    prizetime = models.FloatField(verbose_name=FoundationConst.VN_PRITIME, null=True, blank=True, default=None)
    usrprizes = models.CharField(verbose_name=FoundationConst.VN_USRPRI, null=True, blank=True, max_length=100, default=None)

    class Meta:
        verbose_name = UserPhonecallConst.VN_TABLE_NAME
        verbose_name_plural = UserPhonecallConst.VN_TABLE_NAME

    def __unicode__(self):
        return str(self.id)


class addCode(models.Model):
    creatime = models.DateTimeField(auto_now_add=True, verbose_name=u'上传时间')
    File = models.FileField(upload_to="", verbose_name=u'奖品文件')
    issuccess = models.IntegerField(verbose_name=u'状态', choices=WorkConst.IS_FINISH, default=WorkConst.NO_FINISH)

    class Meta:
        verbose_name = AddCode.VN_TABLE_NAME
        verbose_name_plural = AddCode.VN_TABLE_NAME


    def __unicode__(self):
        return str(self.id)


class qrcount(models.Model):
    code = models.CharField(verbose_name=u'奖品码', max_length=300)
    passwd = models.CharField(verbose_name=u'密码', max_length=300)
    qrimg = models.ImageField(upload_to='', verbose_name=u'二维码')
    startime = models.CharField(verbose_name=u'起始时间', max_length=300)
    endtime = models.CharField(verbose_name=u'结束时间', max_length=200)
    isend = models.IntegerField(verbose_name=u'是否发出', choices=WorkConst.send_choice, default=1)
    addtime = models.DateTimeField(auto_now_add=True, verbose_name=u'增加时间')
    openid = models.CharField(null=True, blank=True, verbose_name=u'获奖openid', max_length=300)
    sendTime = models.CharField(verbose_name=u'发卷时间', null=True, blank=True, max_length=100)

    class Meta:
        verbose_name = AddCode.RN_TABLE_NAME
        verbose_name_plural = AddCode.RN_TABLE_NAME

    def __unicode__(self):
        return str(self.id)



class walkCount(models.Model):
    walk = models.IntegerField(verbose_name=u'步数')
    money = models.CharField(max_length=300, verbose_name=u'金额')
    image = models.ImageField(upload_to="", verbose_name=u'图片')
    openid = models.CharField(verbose_name=u'openid', max_length=100)
    change = models.IntegerField(verbose_name=u'更改步数')
    weekMatch = models.IntegerField(verbose_name=u'周次')
    isGet = models.IntegerField(verbose_name=u'是否得过奖品',default=0)
    creaTime = models.DateTimeField(verbose_name=u'上传时间', auto_now_add=True)
    info = models.ForeignKey(UsrPhoneCall, verbose_name=u'联系方式')
    priCode = models.CharField(verbose_name=u'奖品码', null=True, blank=True, max_length=300)

    class Meta:
        verbose_name = ActiveDataConst.VN_TABLE_NAME
        verbose_name_plural = ActiveDataConst.VN_TABLE_NAME

    def __unicode__(self):
        return str(self.id)


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
        return str(self.openid)



class AdminLog(models.Model):
    usrname = models.CharField(verbose_name=u'管理员', max_length=100)
    event = models.CharField(verbose_name=u'事件', max_length=300)
    eventime = models.DateTimeField(verbose_name=u'时间', auto_now_add=True)

    class Meta:
        verbose_name = u'行为日志'
        verbose_name_plural = u'行为日志'

    def __unicode__(self):
        return str(self.usrname)


class hitprize(models.Model):
    creatime = models.DateTimeField(auto_now_add=True, verbose_name=u'生成时间')
    countType = models.IntegerField(verbose_name=u'排名方式', choices=FoundationConst.COUNT_CHOICES)
    isSend = models.IntegerField(verbose_name=u'是否发出', choices=FoundationConst.SEND_CHOICES, default=FoundationConst.NO_SEND)
    weekMacht = models.IntegerField(verbose_name=u'周次', null=True, blank=True)

    class Meta:
        verbose_name = u'中奖信息'
        verbose_name_plural = u'中奖信息'

    def __unicode__(self):
        return str(self.creatime)


class weekCount(models.Model):
    weekMatch = models.IntegerField(verbose_name=u'周次')
    openid = models.CharField(verbose_name=u'用户openid', max_length=300)
    walk = models.IntegerField(verbose_name=u'步数总数')
    isSend = models.IntegerField(verbose_name=u'是否发奖', default=0)

    class Meta:
        verbose_name = u'周排行步数'
        verbose_name_plural = u'周排行步数'



class AdminUser(models.Model):
    username = models.CharField(verbose_name=u"管理员昵称", max_length=100)
    userpasswd = models.CharField(verbose_name=u"密码", max_length=100)

    class Meta:
        verbose_name = u"后台管理员账户"
        verbose_name_plural = u"后台管理员账户"

    def __unicode__(self):
        return str(self.username)






class CountPUV(models.Model):
    pv = models.CharField(max_length=200, default="0", verbose_name=FoundationConst.VN_PV)
    uv = models.CharField(max_length=200, default="0", verbose_name=FoundationConst.VN_UV)
    addpv = models.CharField(max_length=200, default="0", verbose_name=FoundationConst.VN_FAKEPV)
    adduv = models.CharField(max_length=200, default="0", verbose_name=FoundationConst.VN_FAKEUV)




class PageView(models.Model):
    url = models.URLField(verbose_name=FoundationConst.VN_URL)
    ip = models.GenericIPAddressField(verbose_name=FoundationConst.VN_IP)
    creationTime = models.DateTimeField(auto_now_add=True, verbose_name=FoundationConst.VN_CREATION_TIME)


    class Meta:
        verbose_name = PageViewConst.VN_TABLE_NAME
        verbose_name_plural = PageViewConst.VN_TABLE_NAME

    def __unicode__(self):
        return str(self.id)


class UniqueVisitor(models.Model):
    url = models.URLField(verbose_name=FoundationConst.VN_URL)
    wxUser = models.ForeignKey(WXUser, null=True, blank=True, verbose_name=WXUserConst.VN_TABLE_NAME)
    ip = models.GenericIPAddressField(verbose_name=FoundationConst.VN_IP)
    creationTime = models.DateTimeField(auto_now_add=True, verbose_name=FoundationConst.VN_CREATION_TIME)

    class Meta:
        verbose_name = UniqueVisitorConst.VN_TABLE_NAME
        verbose_name_plural = UniqueVisitorConst.VN_TABLE_NAME

    def __unicode__(self):
        return str(self.id)