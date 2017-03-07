# -*- coding: utf-8 -*-
from campaigns.liantong.applet.decorators import page_render, auth_verification, pv,uv
from campaigns.liantong.config import ViewConfig
from campaigns.liantong .applet.Get_Auth_verification import _Auth_view
from django.http import HttpResponseRedirect



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def share(request):
    pass




@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def index(request):
    pass



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "success.html")
def success(request):
    pass



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "upload.html")
def upload(request):
    pass


@uv
@pv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def IndexNew(request):
    pass




@uv
@pv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def lizhi(request):
    pass



@uv
@pv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def LJL(request):
    pass



@uv
@pv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def ddbb(request):
    pass



@uv
@pv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def BRN(request):
    pass





@uv
@pv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def XDKB(request):
    pass


@page_render(ViewConfig.TEMPLATE_PC_URL + "index.html")
def PCindex(request):
    pass


@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "vote.html")
def mobileVote(request):
    pass



@page_render(ViewConfig.TEMPLATE_PC_URL + "login.html")
def PClogin(request):
    pass



@pv
@uv
def selfUrl(request):
    return HttpResponseRedirect("http://8dd2a40211dc.ih5.cn/idea/g-aESl3")




@uv
@pv
def lTURl(request):
    return HttpResponseRedirect("http://8dd2a40211dc.ih5.cn/idea/g-aESl3")



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def Nanjing(request):
    pass



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def suzhou(request):
    pass




@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def Wuxi(request):
    pass




@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def ChangZhou(request):
    pass




@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def zhengjiang(request):
    pass




@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def NanTong(request):
    pass




@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def TaiZhou(request):
    pass




@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def Yangzhou(request):
    pass



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def YanCheng(request):
    pass



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def HuaiAn(request):
    pass



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def SuQian(request):
    pass


@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def XuZhou(request):
    pass



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def LianYunGang(request):
    pass


@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def jstv(request):
    pass


@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "picc.html")
def picc(request):
    pass


@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "touch.html")
def touch(request):
    pass


@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "news1.html")
def news1(request):
    pass



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "news2.html")
def news2(request):
    pass


@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "news3.html")
def news3(request):
    pass




@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "news4.html")
def news4(request):
    pass



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "news5.html")
def news5(request):
    pass





@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "news6.html")
def news6(request):
    pass




@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "news7.html")
def news7(request):
    pass




@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "news8.html")
def news8(request):
    pass


@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "jt.html")
def jt(request):
    pass



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "jt_new_year.html")
def jt_kuanian(request):
    pass

@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "jt_two.html")
def jt_airport(request):
    pass



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "wo1223.html")
def wo1223(request):
    pass



@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "yh_app.html")
def yh_app(request):
    pass


@pv
@uv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "lt_new.html")
def lt_new(request):
    pass