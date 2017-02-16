# -*- coding: utf-8 -*-
from campaigns.qc.applet.decorators import page_render, auth_verification, pv
from campaigns.qc.config import ViewConfig
from campaigns.qc .applet.Get_Auth_verification import _Auth_view

@page_render(ViewConfig.TEMPLATE_PC_URL + "qiche_lz.html")
def qicheIndex(request):
    pass