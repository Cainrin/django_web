#coding=utf-8
import urllib2, urllib
import hashlib
import time
import hmac
import random
import base64
import binascii


class Auth(object):
    def __init__(self):
        self.appid = "10030008"
        self.secret_id = "AKIDLMiPp9s40iDyGlzsULO6izGZICDuujJw"
        self.secret_key = "DvpK3udaFkI9XaBxshirtgTGEma6A26N"



    def appSignBase(self, appid, seretid, seretkey, expired, fileid, bucketName):
        now = int(time.time())
        rdm = random.randint(0, 1000000)
        data = "a={0}&k={1}&e={2}&t={3}&r={4}&f={5}&b={6}".format(appid, seretid, expired, now, rdm, fileid, bucketName)
        _bin = hmac.new(seretkey, data, hashlib.sha1).hexdigest()
        _bin = binascii.unhexlify(_bin)
        _bin = _bin + data
        sign = base64.b64encode(_bin, altchars='-_')
        return sign



    def appSign(self, expired, bucketName):
        appid = self.appid
        secretid = self.secret_id
        secretkey = self.secret_key
        return self.appSignBase(appid=appid, seretid=secretid, seretkey=secretkey, expired=expired, fileid="", bucketName=bucketName)




    def appSign_once(self, path, bucketName):
        appid = self.appid
        secretid = self.secret_id
        secretkey = self.secret_key
        if "/" not in path:
            path = "/" + path
        fileid = "/" + appid + "/" + bucketName + path

        return self.appSignBase(appid=appid, seretid=secretid, seretkey=secretkey, expired=0, fileid=fileid, bucketName=bucketName)

