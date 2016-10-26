# -*- coding: utf-8 -*-
from campaigns.hypro.applet.decorators import page_render, auth_verification, pv
from campaigns.hypro.config import ViewConfig
from campaigns.hypro.applet.Get_Auth_verification import _Auth_view


@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def zhIndex(request):
    pass



@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "touch.html")
def zhTouch(request):
    pass


@page_render(ViewConfig.TEMPLATE_PC_URL + "index.html")
def zhPcindex(request):
    pass



@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "ticai.html")
def ticaiIndex(request):
    pass


@page_render(ViewConfig.TEMPLATE_PC_URL + "locta.html")
def locta(request):
    pass


@page_render(ViewConfig.TEMPLATE_PC_URL + "ticaiIndex.html")
def ticaizhuanti(request):
    pass


@page_render(ViewConfig.TEMPLATE_PC_URL + "zhonghangpc.html")
def zhonghangpc(request):
    pass


@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "ticainew.html")
def ticainew(request):
    pass