# -*- coding: utf-8 -*-
import datetime
import time
import random
from campaigns.foundation.applet import response, utils
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.qiche import models, config, const
from campaigns.foundation import wechat_api
from campaigns.qiche.applet import decorators, POSTCONN
from campaigns.qiche.applet.uitls import fit_up_work_list, save_work_image, fit_up_work
from campaigns.qiche.applet import cos
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


@decorators.action_render
def revcdata(request):
    key = request.POST['Key']
    LEAD_TYPE = request.POST['LEAD_TYPE']
    USER_KEY = request.POST['USER_KEY']
    MEDIA_LEAD_ID = request.POST['MEDIA_LEAD_ID']
    CUSTOMER_NAME = request.POST['CUSTOMER_NAME']
    FK_DEALER_ID = request.POST['FK_DEALER_ID']
    GENDER = request.POST['GENDER']
    MOBILE = request.POST['MOBILE']
    CITY = request.POST['CITY']
    PROVINCE = request.POST['PROVINCE']
    SERIES = request.POST['SERIES']
    MODEL = request.POST['MODEL']
    BUY_PLAN_TIME_CODE = request.POST['BUY_PLAN_TIME_CODE']
    data = {
        'Key': key,
        'RequestObjectList': [{
            'LEAD_TYPE': LEAD_TYPE,
            'USER_KEY': USER_KEY,
            'MEDIA_LEAD_ID': MEDIA_LEAD_ID,
            'CUSTOMER_NAME': CUSTOMER_NAME,
            'FK_DEALER_ID': FK_DEALER_ID,
            'GENDER': GENDER,
            'MOBILE': MOBILE,
            'CITY': CITY,
            'PROVINCE': PROVINCE,
            'SERIES': SERIES,
            'MODEL': MODEL,
            'BUY_PLAN_TIME_CODE': BUY_PLAN_TIME_CODE
        }]
    }
    usrname = "name: {0}, city: {1}, series: {2}, tel: {3}".format(CUSTOMER_NAME.decode("utf-8"), CITY.decode("utf-8"), SERIES.decode("utf-8"), MOBILE.decode("utf-8"))
    ip = " ip: {0}.{1}.{2}.{3}".format(str(random.randint(1, 253)), str(random.randint(1, 253)), str(random.randint(1, 253)), str(random.randint(1, 253)))
    print usrname
    try:
        database = models.Data.objects.create(
            data=str(usrname) + str(ip)
        )
        senddata = POSTCONN.Webservice(data)
        return {"result_code": 0, "result_msg": str(senddata)}
    except Exception as e:
        print e
        return {"result_code": 1, "result_msg": str(e)}