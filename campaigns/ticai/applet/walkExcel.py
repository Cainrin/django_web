# -*- coding: utf-8 -*-
import time, datetime
from campaigns.ticai.applet.decorators import auth_verification, antExcel, exportExcel
from campaigns.ticai import models


class countDay(object):
    def __init__(self, request=None):
        self.request = request


    def getData(self):
        walkData = models.walkCount.objects.all()
        l1 = []
        for i in walkData:
            d1 = {}
            d1["creatime"] = str(str(i.creaTime).split(" ")[0])
            d1['openid'] = i.openid
            if i.change == i.change:
                d1['walk'] = i.walk
            else:
                d1['walk'] = i.change
            l1.append(d1)
        return l1

    def sortData(self):
        dataList = self.getData()
        dataList = sorted(dataList, key=lambda x: x['creatime'])
        return dataList

    def rankCount(self):
        dataList = self.sortData()
        l1 = []
        l1.append(dataList[0])
        d2 = {}
        for i in dataList:
            l2 = [ j['openid'] for j in l1 ]
            if i['openid'] not in l2:
                l1.append(i)
        for i in l1:
            if not d2.has_key(i['creatime']):
                d2[i['creatime']] = {'usercount': 1}
            else:
                nowCount = d2[i['creatime']]['usercount'] + 1
                d2[i['creatime']] = {'usercount': nowCount}
        return d2

    def finishCount(self):
        valueList = self.rankCount()
        l1 = []
        for i, j in zip(valueList.keys(), valueList.values()):
            tomorrow = str(datetime.date.fromtimestamp(time.mktime(time.strptime(i, "%Y-%m-%d"))) + datetime.timedelta(days=1))
            nowdayUser = models.walkCount.objects.filter(creaTime__gte=i).filter(creaTime__lt=str(tomorrow)).all().count()
            nowday = models.walkCount.objects.filter(creaTime__gte=i).filter(creaTime__lt=str(tomorrow)).all()
            walk = 0
            money = 0
            for l in nowday:
                walk += int(l.change)
            d1 = {}
            money += round(float(walk) / 2000, 2)
            d1['当天PV'] = models.PageView.objects.filter(creationTime__gte=i).filter(creationTime__lt=tomorrow).all().count()
            d1['当天UV'] = models.WXUser.objects.filter(creationTime__gte=i).filter(creationTime__lt=tomorrow).all().count()
            d1['时间'] = i
            d1['新增用户'] = j['usercount']
            d1['当天用户总数'] = nowdayUser
            d1['总步数'] = walk
            d1['捐赠金额'] = money
            l1.append(d1)
        return l1

    def startDraw(self):
        valueList = self.finishCount()
        if self.request is None:
            pushExcel = antExcel("数据单", valueList)
        else:
            pushExcel = exportExcel(self.request, "数据单", valueList)
        return pushExcel

