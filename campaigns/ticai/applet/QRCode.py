import qrcode, uuid
from cmp import settings
from campaigns.ticai.config import WorkConfig
from campaigns.ticai import models

class addQRCODE(object):

    def __init__(self, filePath):
        self.FilePath = filePath
    def startDraw(self):
        try:
            with open(settings.MEDIA_ROOT + self.FilePath, "r") as f:
                for i in f.readlines():
                    code = i.split(",")[0]
                    passwd = code[-4: ]
                    startime = i.split(',')[2]
                    endtime = i.split(',')[3]
                    str1 = "2A" + code
                    img = qrcode.make(str1)
                    imgName = "{0}{1}.{2}".format(WorkConfig.REL_PATH_IMAGE, uuid.uuid4().hex, "png")
                    img.save(settings.MEDIA_ROOT + imgName)
                    models.qrcount.objects.create(
                        code=code,
                        passwd=passwd,
                        startime=startime,
                        endtime=endtime,
                        qrimg=imgName
                    )
            return "success"
        except Exception as e:
            return str(e)