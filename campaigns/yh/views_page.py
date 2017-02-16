# -*- coding: utf-8 -*-
from campaigns.yh.applet.decorators import page_render, auth_verification, pv, uv
from campaigns.yh.config import ViewConfig
from campaigns.yh.applet.Get_Auth_verification import _Auth_view
import models
from django.http import HttpResponseRedirect


@uv
@pv
@auth_verification
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def index(request):
    pass



@uv
@pv
@auth_verification
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "main.html")
def Main(request):
    pass



@uv
@pv
@auth_verification
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "success.html")
def success(request):
    pass




@uv
@pv
@auth_verification
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "share.html")
def share(request):
    pass




@uv
@pv
@auth_verification
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "upload.html")
def upload(request):
    pass



@pv
@uv
@auth_verification
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index_2.html")
def index2(request):
    pass




@pv
@uv
@auth_verification
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "work.html")
def Work(request):
    pass





@uv
@pv
@auth_verification
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "workList.html")
def WorkList(request):
    pass






@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "uploadNew.html")
def fakeUp(request):
    pass