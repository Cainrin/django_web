var WX_share=function(){
			var	IndexUrl=window.location.href;	
			var Url="http://fanta.kuh5.net/ticai/index";
			var  TT='体彩测试标题';
			var ImgUrl='http://fanta.kuh5.net/static/campaigns/ticai/mobile/image/shakeimg.png';
			var Desc='体彩测试文案';
			$.ajax({
				type: "POST",
				url: "http://fanta.kuh5.net/ticai/get_sign_package",
				data: {
					url:IndexUrl
				},
				async: !0,
				dataType: "json",
				success: function(a) {
					if (a) {
						var nonceStr = a["nonceStr"],
							timestamp = a["timestamp"],
							signature = a["signature"],
							mpappid = a["appId"];
						wx.config({
							debug:false,
							appId: mpappid,
							timestamp: timestamp,
							nonceStr: nonceStr,
							signature: signature,
							jsApiList: ["onMenuShareAppMessage", "onMenuShareTimeline", "onMenuShareQQ", "onMenuShareWeibo", "onMenuShareQZone","addCard","checkJsApi" ]
						});
						wx.ready(function() {
							
							wx.onMenuShareTimeline({
								title:TT ,
								desc: Desc,
								link: Url,
								imgUrl: ImgUrl,
								success:function(){
									//shareUpdate();
								}
							});
							wx.onMenuShareAppMessage({
								title: TT,
								desc: Desc,
								link: Url,
								imgUrl:ImgUrl,
								success:function(){
									//shareUpdate();
								}
							});
							wx.onMenuShareQQ({
								title: TT,
								desc: Desc,
								link: Url,
								imgUrl: ImgUrl,
								success:function(){
									//shareUpdate();
								}
							});
							wx.onMenuShareWeibo({
								title: TT,
								desc: Desc,
								link: Url,
								imgUrl: ImgUrl,
								success:function(){
									//shareUpdate();
								}
							});
							wx.onMenuShareQZone({
								title: TT,
								desc: Desc,
								link: Url,
								imgUrl: ImgUrl,
								success:function(){
									//shareUpdate();
								}
							});
							wx.checkJsApi({
							   jsApiList: [
							   'addCard','onMenuShareTimeline','onMenuShareAppMessage','onMenuShareQQ','onMenuShareWeibo','onMenuShareQZone'
							   ],
							   success: function (res) {
							   		var t = res.checkResult.addCard;
							   		//判断checkJsApi 是否成功 以及 wx.config是否error
							   		}
							})
						})
					}
				},
				error: function(a, b) {}
			})
	};

var shareUpdate = function () {
	var	IndexUrl=window.location.href;
	$.ajax({
				type: "POST",
				url: "http://fanta.kuh5.net/picc/mobile/mobile_share",
				data: {
					url:IndexUrl
				},
				async: !0,
				dataType: "json",
				success: function(a) {
				},
				error: function(a, b) {}
			})
}

var browser = {
    versions: function () {
        var u = navigator.userAgent, app = navigator.appVersion;
        return {         //移动终端浏览器版本信息
            trident: u.indexOf('Trident') > -1, //IE内核
            presto: u.indexOf('Presto') > -1, //opera内核
            webKit: u.indexOf('AppleWebKit') > -1, //苹果、谷歌内核
            gecko: u.indexOf('Gecko') > -1 && u.indexOf('KHTML') == -1, //火狐内核
            mobile: !!u.match(/AppleWebKit.*Mobile.*/), //是否为移动终端
            ios: !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/), //ios终端
            android: u.indexOf('Android') > -1 || u.indexOf('Linux') > -1, //android终端或uc浏览器
            iPhone: u.indexOf('iPhone') > -1, //是否为iPhone或者QQHD浏览器
            iPad: u.indexOf('iPad') > -1, //是否iPad
            webApp: u.indexOf('Safari') == -1 //是否web应该程序，没有头部与底部
        };
    }(),
    language: (navigator.browserLanguage || navigator.language).toLowerCase()
}


if (browser.versions.mobile) {//判断是否是移动设备打开。browser代码在下面
        var ua = navigator.userAgent.toLowerCase();//获取判断用的对象
        if (ua.match(/MicroMessenger/i) == "micromessenger") {
                //在微信中打开
               //分享	
			WX_share();	
        }
        if (ua.match(/WeiBo/i) == "weibo") {
                //在新浪微博客户端打开
        }
        if (ua.match(/QQ/i) == "qq") {
                //在QQ空间打开
        }
        if (browser.versions.ios) {
                //是否在IOS浏览器打开
        } 
        if(browser.versions.android){
                //是否在安卓浏览器打开
        }
	} 
	else {
	        //否则就是PC浏览器打开
	}
//分享

