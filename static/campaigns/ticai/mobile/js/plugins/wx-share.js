var WX_share=function(){
//			var Walk=sessionStorage.getItem('dangqiwalk');
//			var Openid=sessionStorage.getItem('Openid');
//			var imgName;
//			alert(Walk)
//			var Url="http://fanta.kuh5.net/testticai/shareIndex?Openid="+Openid;
//			if(Walk>0 && Walk<3000){
//				imgName=1;
//			}else if(Walk>=3000 && Walk<=3999){
//				imgName=2;
//			}else if($scope.count>=4000 && Walk<=6999){
//				imgName=3;
//			}else if($scope.count>=7000 && Walk<=9999){
//				imgName=4;
//			}
//			else if(Walk>=10000 && Walk<=1999){
//				imgName=5;
//			}
//			else if(Walk>=20000){
//				imgName=6;
//			}else{
//				imgName=7;
//				Url="http://fanta.kuh5.net/testticai/index";
//			}
	        var Url="http://fanta.kuh5.net/ticai/index";
			var	IndexUrl=window.location.href;	
			
			var  TT='体彩爱行走';
			//var ImgUrl='http://fanta.kuh5.net/static/campaigns/ticai/mobile/image/1/'+imgName+'.png';
			var ImgUrl='http://fanta.kuh5.net/static/campaigns/ticai/mobile/image/share/7.png';
			var Desc='江苏体彩爱行走第二季，向不可能说“步”！';
			$.ajax({
				type: "POST",
				url: "http://fanta.kuh5.net/ticai/get_sign_package",
				data: {
					url:IndexUrl
				},
				async: !0,
				dataType: "json",
				success: function(a) {
					//alert(JSON.stringify(a))
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
								}
							});
							wx.onMenuShareAppMessage({
								title: TT,
								desc: Desc,
								link: Url,
								imgUrl:ImgUrl,
								success:function(){
									//alert('分享成功')
								}
							});
							wx.onMenuShareQQ({
								title: TT,
								desc: Desc,
								link: Url,
								imgUrl: ImgUrl,
								success:function(){
								}
							});
							wx.onMenuShareWeibo({
								title: TT,
								desc: Desc,
								link: Url,
								imgUrl: ImgUrl,
								success:function(){
								}
							});
							wx.onMenuShareQZone({
								title: TT,
								desc: Desc,
								link: Url,
								imgUrl: ImgUrl,
								success:function(){
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
				url: "http://fanta.kuh5.net/ticai/mobile/mobile_share",
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

