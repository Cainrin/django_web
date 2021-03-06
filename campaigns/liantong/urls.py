# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from campaigns.liantong import views_page, views_action


urlpatterns = [
    url(r'^tocloud', views_action.tocloud),
    url(r'^getlocation', views_action.getLocation),
    url(r'^upload', views_action.uploadPage),
    url(r'^mobile/get_sign_package', views_action.get_sign_package),
    url(r'^getExcel$', views_action.getExcel),
    url(r'^backadmin$', views_action.backadmin),
    url(r'^status$', views_action.changeStatus),
    url(r'^mobile/index.html$', views_page.index),
    url(r'^mobile/success.html$', views_page.success),
    url(r'^mobile/upload.html$', views_page.upload),
    url(r'^mobile/IndexNew.html$', views_page.IndexNew),
    url(r'^mobile/check$', views_action.checkUp),
    url(r'^mobile/lizhi.html$', views_page.lizhi),
    url(r'^mobile/lingjuli.html$', views_page.LJL),
    url(r'^mobile/ddbb.html$', views_page.ddbb),
    url(r'^mobile/boruina.html$', views_page.BRN),
    url(r'^mobile/xiandai.html$', views_page.XDKB),
    url(r'^mobile/share.html$', views_page.share),
    url(r'^mobile/self.html$', views_page.selfUrl),
    url(r'^mobile/ljl.html$', views_page.lTURl),
    url(r'^mobile/vote.html$', views_page.mobileVote),
    url(r'^fakedata$', views_action.fakedata),
    url(r'^back/index.html$', views_page.PCindex),
    url(r'^back/login$', views_action.AdminLogIn),
    url(r'^back/login.html$', views_page.PClogin),
    url(r'^back/getExcel$', views_action.getyestExcel),
    url(r'^ltUpload$', views_action.ltUpload),
    url(r'^mobile/nanjing$', views_page.Nanjing),
    url(r'^mobile/suzhou$', views_page.suzhou),
    url(r'^mobile/wuxi$', views_page.Wuxi),
    url(r'^mobile/changzhou$', views_page.ChangZhou),
    url(r'^mobile/zhengjiang$', views_page.zhengjiang),
    url(r'^mobile/nantong$', views_page.NanTong),
    url(r'^mobile/taizhou$', views_page.TaiZhou),
    url(r'^mobile/yangzhou$', views_page.Yangzhou),
    url(r'^mobile/yancheng$', views_page.YanCheng),
    url(r'^mobile/huaian$', views_page.HuaiAn),
    url(r'^mobile/suqian$', views_page.SuQian),
    url(r'^mobile/xuzhou$', views_page.XuZhou),
    url(r'^mobile/lianyungang$', views_page.LianYunGang),
    url(r'^picc$', views_page.picc),
    url(r'^mobile/jstv$', views_page.jstv),
    url(r'^mobile/touch.html$', views_page.touch),
    url(r'^mobile/news1.html$', views_page.news1),
    url(r'^mobile/news2.html$', views_page.news2),
    url(r'^mobile/news3.html$', views_page.news3),
    url(r'^mobile/news4.html$', views_page.news4),
    url(r'^mobile/news5.html$', views_page.news5),
    url(r'^mobile/news6.html$', views_page.news6),
    url(r'^mobile/news7.html$', views_page.news7),
    url(r'^mobile/news8.html$', views_page.news8),
    url(r'^mobile/signup$', views_action.userInfo),
    # url(r'^mobile/jt.html$', views_page.jt),
    url(r'^mobile/wo1223.html$', views_page.wo1223),
    # url(r'^mobile/jtkn.html$', views_page.jt_kuanian),
    # url(r'^mobile/jtjc.html$', views_page.jt_airport),
    url(r'^mobile/yhapp.html', views_page.yh_app),
]