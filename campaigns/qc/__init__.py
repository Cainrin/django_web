# -*- coding: utf-8 -*-
import os
from campaigns.foundation.models import Campaign

default_app_config = 'campaigns.qc.apps.QcConfig'
app_id = 21
# app_id = Campaign.objects.filter(appName=os.path.dirname(os.path.abspath(__file__)).replace("\\", "/").split("/")[-1])[0].id

