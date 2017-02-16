# -*- encoding: utf-8 -*-
import random, datetime, pytz
from campaigns.ticai import config
from django.utils import timezone
import Send
from campaigns.foundation.const import FoundationConst
from campaigns.ticai import const, models

class SendPriceProcess(Send.CheatProcess):
    def __init__(self, vote_cheat):
        self.vote_cheat = vote_cheat
        self.result_reason = None
        now = datetime.date.today()
        PRICESINFO = models.hitprize.objects.filter(creatime__gte=now).filter(countType=1).all()
        weekDay = now - datetime.timedelta(days=1)
        if not PRICESINFO:
            self.result_reason = "error"
            self.vote_cheat.hasFinished = True
            self.vote_cheat.save()
        else:
            weekCount = PRICESINFO[0].weekMacht
            nowday = datetime.date.today()
            now = timezone.datetime.now()
            priceCount = models.qrcount.objects.filter(isend=1).filter(startime=str(datetime.date.today())).all()
            if not priceCount:
                self.result_reason = "没有奬卷"
                self.vote_cheat.hasFinished = True
                self.vote_cheat.save()
            if weekCount == 1:
                startTime = datetime.datetime.utcfromtimestamp(config.WorkConfig.starTime)
                startTime = datetime.datetime(startTime.year, startTime.month, startTime.day, 0, 0, 0, tzinfo=pytz.utc)
            elif weekCount == 2:
                startTime = datetime.datetime.utcfromtimestamp(config.WorkConfig.starTime)
                startTime = datetime.datetime(startTime.year, startTime.month, startTime.day, 0, 0, 0, tzinfo=pytz.utc) \
                            + datetime.timedelta(days=7)
            else:
                startTime = datetime.datetime.utcfromtimestamp(config.WorkConfig.starTime)
                startTime = datetime.datetime(startTime.year, startTime.month, startTime.day, 0, 0, 0,
                                              tzinfo=pytz.utc) + datetime.timedelta(days=14)
            priceList = []
            self.vote_cheat.totalCount = models.walkCount.objects.filter(creaTime__gte=weekDay, creaTime__lt=nowday, isGet=0, change__gt=0, info__usractive__isnull=False).order_by(
                    '-change', 'creaTime').all()
            if self.vote_cheat.totalCount.count() > 3000:
                Tcount = 3000
                self.vote_cheat.totalCount = 3000
            else:
                Tcount = self.vote_cheat.totalCount.count()
            interval_seconds = float(self.vote_cheat.minute) * 60 / float(Tcount)
            super(SendPriceProcess, self).__init__(interval_seconds, Tcount)

    def cheat(self):
        nowday = datetime.date.today()
        weekDay = nowday - datetime.timedelta(days=1)
        price = models.qrcount.objects.filter(isend=1).filter(startime=str(datetime.date.today()))
        work = models.walkCount.objects.filter(creaTime__gte=weekDay, creaTime__lt=nowday, isGet=0, change__gt=0, info__usractive__isnull=False).order_by(
                    '-change', 'creaTime')
        if work.first() is None:
            self.result_reason = "已发完"
            self.vote_cheat.hasFinished = True
            self.vote_cheat.save()
            return False
        elif price.first() is None:
            self.result_reason = "没有奬卷"
            self.vote_cheat.save()
            return False
        else:
            todayInfo = models.walkCount.objects.filter(creaTime__gte=datetime.date.today()).filter(
                weekMatch=work[0].weekMatch).filter(openid=work[0].openid)
            if todayInfo.first() is not None:
                todayInfo.update(isGet=1)

            models.walkCount.objects.filter(id=work[0].id).update(priCode=price.first().id, isGet=1)
            now = datetime.datetime.now()
            models.qrcount.objects.filter(id=price[0].id).update(isend=0, sendTime=now)
        self.vote_cheat.nowCount += 1
        self.vote_cheat.save()

    def cheat_finished(self):
        now = datetime.date.today()
        models.hitprize.objects.filter(creatime__gte=now).filter(countType=1).update(isSend=0)
        self.vote_cheat.hasFinished = True
        self.vote_cheat.FinishedReason = self.result_reason
        self.vote_cheat.save()