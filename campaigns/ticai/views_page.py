# -*- coding: utf-8 -*-
from campaigns.ticai.applet.decorators import page_render, auth_verification, pv
from campaigns.ticai.config import ViewConfig
from campaigns.ticai.applet.Get_Auth_verification import _Auth_view


@auth_verification
@pv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "about.html")
def about(request):
    pass


@auth_verification
@pv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def index(request):
    pass


@auth_verification
@pv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "shareIndex.html")
def shareIndex(request):
    pass


@auth_verification
@pv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "success.html")
def success(request):
    pass



@auth_verification
@pv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "upload.html")
def vsupload(request):
    pass


@pv
@page_render(ViewConfig.TEMPLATE_PC_URL + "index.html")
def backIndex(request):
    pass


@pv
@page_render(ViewConfig.TEMPLATE_PC_URL + "login.html")
def backLogin(request):
    pass