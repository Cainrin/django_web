# -*- coding: utf-8 -*-
import os
from campaigns.foundation.models import Campaign

default_app_config = 'campaigns.jsblank.apps.JsConfig'
app_id = 23
# app_id = Campaign.objects.filter(appName=os.path.dirname(os.path.abspath(__file__)).replace("\\", "/").split("/")[-1])[0].id

