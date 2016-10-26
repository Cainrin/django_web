# -*- coding: utf-8 -*-
import qcloud_cos, os
from django.conf import settings
from campaigns.foundation.const import FoundationConst
from campaigns.foundation.applet import utils


class TxCos(object):
    def __init__(self):
        cos_info = settings.QCLOUD_COS
        app_id = cos_info[FoundationConst.QCLOUD_COS_APP_ID]
        secret_id = cos_info[FoundationConst.QCLOUD_COS_SECRET_ID]
        secret_key = cos_info[FoundationConst.QCLOUD_COS_SECRET_KEY]
        self.cos = qcloud_cos.Cos(app_id, secret_id, secret_key)
        self.bucket = cos_info[FoundationConst.QCLOUD_COS_BUCKET]

    def _need_create_folder(self, cos_path):
        result = self.cos.statFolder(self.bucket, cos_path)
        return result[FoundationConst.RN_CODE] != 0

    def _create_folder(self, cos_path):
        self.cos.createFolder(self.bucket, cos_path)

    def upload_file(self, local_full_filename, cos_full_filename):
        cos_path = os.path.split(cos_full_filename)[0]
        if self._need_create_folder(cos_path):
            self._create_folder(cos_path)
        file_size = os.path.getsize(local_full_filename)
        # 8 * 1024 * 1024 = 8388608
        if file_size < 8388608:
            result = self.cos.upload(local_full_filename, self.bucket, cos_full_filename)
        else:
            result = self.cos.upload_slice(local_full_filename, self.bucket, cos_full_filename)
        if result[FoundationConst.RN_CODE] != 0:
            raise utils.ClientException("{}:{}".format(FoundationConst.QCLOUD_COS_EXCEPTION_UPLOAD_FAILED, result[FoundationConst.RN_MESSAGE]))



