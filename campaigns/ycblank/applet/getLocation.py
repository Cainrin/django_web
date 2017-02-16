# -*- encoding: UTF-8 -*-
import requests
import json



class txLocations(object):
    def __init__(self, location):
        self.location = location
        self.url = "http://apis.map.qq.com/ws/geocoder/v1/"
        self.key = "KUMBZ-FNERI-CRHGM-56E7O-MD2IS-2FBPX"
    def getLocat(self):
        info = requests.get(url=self.url, params={'location': self.location, 'key': self.key})
        return info.json()



# print str(a['result']['address_component']).replace('u\'', '\'').decode("unicode-escape")
