# -*- coding: utf-8 -*-
import time, StringIO, uuid, datetime
from PIL import Image
from django.conf import settings
from campaigns.qc.config import ViewConfig, WorkConfig
from campaigns.foundation.const import FoundationConst


def generate_other_dict_data():
    odd = dict()
    odd[FoundationConst.RN_STATIC_URL] = '{0}'.format('http://qc-10030008.file.myqcloud.com/')
    if settings.DEBUG:
        odd[FoundationConst.RN_WEIXIN_DEBUG] = '?{0}'.format(int(time.time()))
    return odd


def save_work_image(http_chunk):
    filename = http_chunk.name.encode(FoundationConst.ENCODE_UTF8)
    if filename == 'blob':
        filename = 'blob.png'
    mem_file = StringIO.StringIO()
    for chunk in http_chunk.chunks():
        mem_file.write(chunk)
    image = Image.open(mem_file)
    ext = filename.split('.')[-1]
    filename = '{0}{1}.{2}'.format(WorkConfig.REL_PATH_IMAGE, uuid.uuid4().hex, ext)
    image.save(settings.MEDIA_ROOT + filename)
    return filename


def fit_up_work(work):
    dict_work = dict()
    dict_work['workId'] = work.id
    dict_work['workName'] = work.name
    dict_work['workUrl'] = work.image.url
    dict_work['workVotedCount'] = work.votedCount
    dict_work['workCreationTime'] = (work.creationTime + datetime.timedelta(hours=8)).strftime(FoundationConst.EXPORT_DATETIME_MINUTE_FORMAT)
    dict_work['authorName'] = work.author.name
    dict_work['authorSchool'] = work.author.school
    return dict_work


def fit_up_work_list(work_list):
    dict_work_list = list()
    for work in work_list:
        dict_work = fit_up_work(work)
        dict_work_list.append(dict_work)
    return dict_work_list
