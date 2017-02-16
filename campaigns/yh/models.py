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


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name=FoundationConst.VN_NAME, null=True, blank=True)
    cellphone = models.CharField(max_length=50, verbose_name=FoundationConst.VN_CELLPHONE, null=True, blank=True)
    wxUser = models.ForeignKey(WXUser, null=True, blank=True, verbose_name=WXUserConst.VN_TABLE_NAME)
    creationTime = models.DateTimeField(auto_now_add=True, verbose_name=FoundationConst.VN_CREATION_TIME)
    comment = models.CharField(max_length=100, null=True, blank=True, verbose_name=FoundationConst.VN_COMMENT)

    class Meta:
        verbose_name = AuthorConst.VN_TABLE_NAME
        verbose_name_plural = AuthorConst.VN_TABLE_NAME

    def __unicode__(self):
        return str(self.id)


class Work(models.Model):
    name = models.CharField(max_length=100, verbose_name=FoundationConst.VN_NAME)
    string = models.CharField(max_length=300, verbose_name=FoundationConst.VN_STRING)
    imageurl = models.ImageField(upload_to="", verbose_name=FoundationConst.VN_IMAGE)
    author = models.ForeignKey(Author, verbose_name=AuthorConst.VN_TABLE_NAME)
    type = models.IntegerField(choices=WorkConst.TYPE_CHOICES, verbose_name=FoundationConst.VN_TYPE)
    votedCount = models.IntegerField(default=0, verbose_name=FoundationConst.VN_VOTED_COUNT)
    status = models.IntegerField(choices=FoundationConst.STATUS_CHOICES, verbose_name=FoundationConst.VN_STATUS)
    creationTime = models.DateTimeField(auto_now_add=True, verbose_name=FoundationConst.VN_CREATION_TIME)

    class Meta:
        verbose_name = WorkConst.VN_TABLE_NAME
        verbose_name_plural = WorkConst.VN_TABLE_NAME

    def __unicode__(self):
        return str(self.id)


class Share(models.Model):
    url = models.URLField(verbose_name=FoundationConst.VN_URL)
    work = models.ForeignKey(Work, null=True, blank=True, verbose_name=WorkConst.VN_TABLE_NAME)
    platform = models.IntegerField(choices=FoundationConst.PLATFORM_CHOICES, verbose_name=FoundationConst.VN_PLATFORM)
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name=FoundationConst.VN_IP)
    wxUser = models.ForeignKey(WXUser, null=True, blank=True, verbose_name=WXUserConst.VN_TABLE_NAME)
    creationTime = models.DateTimeField(auto_now_add=True, verbose_name=FoundationConst.VN_CREATION_TIME)

    class Meta:
        verbose_name = ShareConst.VN_TABLE_NAME
        verbose_name_plural = ShareConst.VN_TABLE_NAME

    def __unicode__(self):
        return ShareConst.VN_TABLE_NAME

    def save(self, *args, **kwargs):
        if self.work is not None:
            self.work.sharedCount = Share.objects.filter(work=self.work).count() + 1
            self.work.save()
        super(Share, self).save(*args, **kwargs)


class Vote(models.Model):
    work = models.ForeignKey(Work, verbose_name=WorkConst.VN_TABLE_NAME)
    wxUser = models.ForeignKey(WXUser, null=True, blank=True, verbose_name=WXUserConst.VN_TABLE_NAME)
    status = models.IntegerField(choices=FoundationConst.STATUS_CHOICES, verbose_name=FoundationConst.VN_STATUS)
    creationTime = models.DateField(auto_now_add=True, verbose_name=FoundationConst.VN_CREATION_TIME)

    class Meta:
        verbose_name = VoteConst.VN_TABLE_NAME
        verbose_name_plural = VoteConst.VN_TABLE_NAME

    def __unicode__(self):
        return VoteConst.VN_TABLE_NAME

    def save(self, *args, **kwargs):
        self.work.votedCount = Vote.objects.filter(work=self.work).filter(status=FoundationConst.STATUS_ONLINE).count() + 1
        self.work.save()
        super(Vote, self).save(*args, **kwargs)


class VoteCheat(models.Model):
    comment = models.CharField(max_length=100, verbose_name=FoundationConst.VN_COMMENT)
    type = models.IntegerField(choices=VoteCheatConst.TYPE_CHOICES, verbose_name=FoundationConst.VN_TYPE)
    minute = models.IntegerField(verbose_name=FoundationConst.VN_MINUTE)
    totalCount = models.IntegerField(verbose_name=FoundationConst.VN_TOTAL_COUNT)
    nowCount = models.IntegerField(null=True, blank=True, verbose_name=FoundationConst.VN_NOW_COUNT, default=0)
    work = models.ForeignKey(Work, null=True, blank=True, verbose_name=WorkConst.VN_TABLE_NAME)
    ip = models.GenericIPAddressField(verbose_name=FoundationConst.VN_IP, default=FoundationConst.DEFAULT_IP)
    hasFinished = models.BooleanField(verbose_name=FoundationConst.VN_HAS_FINISHED, default=False)
    creationTime = models.DateTimeField(auto_now_add=True, verbose_name=FoundationConst.VN_CREATION_TIME)
    updateTime = models.DateTimeField(auto_now=True, verbose_name=FoundationConst.VN_UPDATE_TIME)

    class Meta:
        verbose_name = VoteCheatConst.VN_TABLE_NAME
        verbose_name_plural = VoteCheatConst.VN_TABLE_NAME

    def __unicode__(self):
        return self.comment


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


class ranDomWork(models.Model):
    imageurl = models.ImageField(upload_to="", verbose_name=FoundationConst.VN_IMAGE)
    rank = models.IntegerField(verbose_name=u'排序')
    crreaTime = models.DateField(auto_now_add=True, verbose_name=FoundationConst.VN_CREATION_TIME)

    def __unicode__(self):
        return str(self.id)