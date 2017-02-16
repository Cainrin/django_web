# -*- coding: utf-8 -*-

"""
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
         佛祖保佑       永无BUG
"""
import random, os
import math
from campaigns.foundation.applet import response, utils
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.nihuawocai import models, config, const
from campaigns.foundation import wechat_api
from campaigns.nihuawocai.applet import decorators
from campaigns.nihuawocai.const import Guess
from dwebsocket import accept_websocket, require_websocket
from dwebsocket import websocket
from campaigns.nihuawocai.applet import Websocket


namelist = [{"isuse": 0, "name": "alex"}, {"isuse": 0, "name": "Allen"}, {"isuse": 0, "name": "cj"}, {"isuse": 0, "name": "cain"}]


@decorators.action_render
def Userlogin(request):
    ServPort = random.randint(10086, 10086)
    odds_number = random.randint(3, 11)
    Odds = models.Guessodds.objects.get(id=odds_number)
    odsid = Odds.id
    __odds = Odds.odds
    request.session[ServPort] = __odds
    print "端口： " + str(ServPort) + "  guessid:  " + str(odsid)

    try:
        return {'port': ServPort, "result_code": 0, "result_msg": None, 'odds': __odds, 'odsid': odsid}
    except Exception as e:
        return {"result_code": 1, "result_msg": str(e)}



@decorators.action_render
def StartWebsocket(request):
    SerPort = request.GET['port']
    ws = os.popen('/usr/local/python27/bin/python /tmp/websocket.py ' + SerPort)
    str1 = ws.read()
    print str1
    try:
        return {"result_code": 0, "result_msg": 1}
    except Exception as e:
        return {"error": str(e)}


@decorators.action_render
def GetAnswer(request):
    _port = request.GET['port']
    _anwser = request.GET['answer']
    if _anwser == request.session.get('oods'):
        os.system('pkill -f ' + _port)
        usrname = request.session.get("username")
        global namelist
        for i in namelist:
            i["isuse"] = 0
        return {'answer': True, 'winer': usrname, "result_code": 0, "result_msg": None}
    else:
        return {'answer': False, "result_code": 0, "result_msg": None, 'winer': None}


@decorators.action_render
def joingame(request):
    odsid = request.GET['odsid']
    oods = models.Guessodds.objects.get(id=odsid)
    request.session['oods'] = oods.odds
    global namelist
    for i in namelist:
        if i["isuse"] == 0:
            request.session["username"] = i['name']
            print request.session['username']
            break
    return {"result_code": 0, "result_msg": None}



