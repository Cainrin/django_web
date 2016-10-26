# -*- coding: utf-8 -*-
import os, datetime, pytz
from django.utils import timezone
from campaigns.foundation.applet.utils import ClientException, ServerException
from campaigns.foundation.const import FoundationConst, DisplayConst, CampaignConst
from campaigns.foundation.models import Campaign


# 投票管理
class VoteManager(object):
    def __init__(self, app_id, work_class, vote_class, wx_user_class, ip_limit_count, weixin_limit_count):
        self.app_id = app_id
        self.WorkClass = work_class
        self.VoteClass = vote_class
        self.WXUserClass = wx_user_class
        self.ip_limit_count = ip_limit_count
        self.weixin_limit_count = weixin_limit_count

    def vote(self, work_id, wx_user=None, ip=None):
        campaign = Campaign.objects.get(pk=self.app_id)
        work = self.WorkClass.objects.get(pk=work_id)
        if campaign is None:
            raise ClientException("{0}:{1}".format(DisplayConst.EXCEPTION_VOTE_CANNOT_FETCH_CAMPAIGN_INFO, self.app_id))
        if work is None or work.status != FoundationConst.STATUS_ONLINE:
            raise ClientException(DisplayConst.EXCEPTION_VOTE_CANNOT_FETCH_WORK_INFO)
        if campaign.hasPaused:
            raise ClientException(DisplayConst.EXCEPTION_VOTE_CAMPAIGN_HAS_PASED)
        if campaign.status == CampaignConst.STATUS_FINISHED:
            raise ClientException(DisplayConst.EXCEPTION_VOTE_CAMPAIGN_HAS_FINISHED)
        if campaign.status == FoundationConst.STATUS_WAITING:
            if self._can_start_campaign(campaign):
                self._start_campaign(campaign)
            else:
                raise ClientException(DisplayConst.EXCEPTION_VOTE_CAMPAIGN_STILL_WAITING)
        elif campaign.status == FoundationConst.STATUS_ONLINE:
            if self._can_stop_campaign(campaign):
                self._stop_campaign(campaign)
                raise ClientException(DisplayConst.EXCEPTION_VOTE_CAMPAIGN_HAS_FINISHED)
        if wx_user is not None:
            if self._is_wx_user_valid(wx_user):
                self._vote_from_weixin(work, wx_user)
        elif ip is not None and self._is_ip_valid(ip):
            self._vote_from_ip(work, ip)
        else:
            raise ClientException(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION)

    def _can_start_campaign(self, campaign):
        now = timezone.now()
        return campaign.startTime < now

    def _start_campaign(self, campaign):
        campaign.status = FoundationConst.STATUS_ONLINE
        campaign.save()

    def _can_stop_campaign(self, campaign):
        now = timezone.now()
        return campaign.endTime < now

    def _stop_campaign(self, campaign):
        campaign.status = FoundationConst.STATUS_BANNED
        campaign.save()

    def _calc_today_start(self):
        now = timezone.now()
        return datetime.datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=pytz.utc)

    def _is_ip_valid(self, ip_addr):
        if self.ip_limit_count <= 0:
            return True
        today_start = self._calc_today_start()
        count = self.VoteClass.objects.filter(ip=ip_addr).filter(creationTime__gte=today_start).count()
        return count < self.ip_limit_count

    def _is_wx_user_valid(self, wx_user):
        if self.weixin_limit_count <= 0:
            return True
        today_start = self._calc_today_start()
        count = self.VoteClass.objects.filter(wxUser=wx_user).filter(creationTime__gte=today_start).count()
        return count < self.weixin_limit_count

    def _vote_from_ip(self, work, ip_addr):
        self.VoteClass.objects.create(
            work=work,
            platform=FoundationConst.PLATFORM_DESKTOP,
            ip=ip_addr,
            status=FoundationConst.STATUS_ONLINE
        )

    def _vote_from_weixin(self, work, wx_user):
        self.VoteClass.objects.create(
            work=work,
            platform=FoundationConst.PLATFORM_WEIXIN,
            wxUser=wx_user,
            status=FoundationConst.STATUS_ONLINE
        )
