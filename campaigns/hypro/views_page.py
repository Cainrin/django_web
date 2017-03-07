# -*- coding: utf-8 -*-
from campaigns.hypro.applet.decorators import page_render, auth_verification, pv, uv
from campaigns.hypro.config import ViewConfig
from campaigns.hypro.applet.Get_Auth_verification import _Auth_view


@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "ticai_2.html")
def ticai2(request):
    pass

@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "zhonghangv2.html")
def zhv2(request):
    pass

@page_render(ViewConfig.TEMPLATE_PC_URL + "zhonghangpcv2.html")
def zPCzhv2(request):
    pass


@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def zhIndex(request):
    pass



@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "lt_new.html")
def lt_new(request):
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


@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "ynd.html")
def ynd(request):
    pass


@pv
@uv
@auth_verification
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "ynd.html")
def wxynd(request):
    pass


@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "test_ynd.html")
def testYnd(request):
    pass


@pv
@uv
@page_render(ViewConfig.TEMPLATE_PC_URL + "ccy.html")
def ccy(request):
    pass