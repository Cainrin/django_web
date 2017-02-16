# -*- coding: utf-8 -*-
from campaigns.jsblank.applet.decorators import page_render, auth_verification, pv, uv
from campaigns.jsblank.config import ViewConfig
from campaigns.jsblank.applet.Get_Auth_verification import _Auth_view


@auth_verification
@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def index(request):
    pass



@page_render(ViewConfig.TEMPLATE_PC_URL + "lbs_back.html")
def lbs_back(request):
    pass


@pv
@uv
@page_render(ViewConfig.TEMPLATE_PC_URL + "ccy.html")
def lbs_ccy(request):
    pass




@auth_verification
@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def share(request):
    pass