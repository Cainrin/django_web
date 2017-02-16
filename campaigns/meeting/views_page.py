# -*- coding: utf-8 -*-
from campaigns.meeting.applet.decorators import page_render, auth_verification, pv
from campaigns.meeting.config import ViewConfig
from campaigns.meeting.applet.Get_Auth_verification import _Auth_view



@auth_verification
@page_render(ViewConfig.TEMPLATE_URL + "index.html")
def index(request):
    pass



@page_render(ViewConfig.TEMPLATE_URL + 'pc.html')
def pc(request):
    pass


@page_render(ViewConfig.TEMPLATE_URL + "draw.html")
def draw(request):
    pass

