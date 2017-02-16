# -*- coding: utf-8 -*-
import time, datetime
from campaigns.jsblank.applet.decorators import auth_verification, antExcel, exportExcel
from campaigns.jsblank import models


class countDay(object):
    def __init__(self, request=None, choice=None):
        self.request = request
        self.choice = choice


    def getData(self):
        if self.choice == 1:
            userData = models.prizePool.objects.all()
        else:
            yestday = datetime.date.today() - datetime.timedelta(days=1)
            userData = models.prizePool.objects.filter(creatime__gte=yestday, creatime__lt=datetime.date.today()).all()
        l1 = []
        for i in userData:
            d1 = {}
            d1['创建时间'] = str(i.creatime).split(" ")[0] + " " + str(i.creatime).split(" ")[1].split(".")[0]
            d1['位置'] = i.location
            if i.peasType == 1:
                TYPE = "金豆子"
            else:
                TYPE = "银豆子"
            d1['苏银豆类型'] = TYPE
            d1['数量'] = i.peasCount
            d1['用户姓名'] = i.user.name
            d1['用户手机号'] = i.user.phone
            d1['用户openid'] = i.user.openid
            l1.append(d1)
        return l1

    def startDraw(self):
        valueList = self.getData()
        if self.request is None:
            pushExcel = antExcel("数据单", valueList)
        else:
            pushExcel = exportExcel(self.request, "数据单", valueList)
        return pushExcel

