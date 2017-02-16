(function($) {
	H.mark = {
		voteA:$('.vote_a'),
		but_1:$('.but1'),
		but_left:$(".but_left"),
		but_right:$(".but_right"),
		$workId:0,
		getWorkId:0,
		init: function() {
			This=this;
			H.mark.getWorkId=getQueryString('workId');
			var Height=$('.em1').height();
			$('.product').height(Height);
			
			This.Pro(H.mark.getWorkId);
			This.Click();
			This.Left_Right();
		},
		Left_Right:function(){
			This=this;
			This.but_left.click(function(){
				$('.img_a .em1').addClass('vH').siblings('em').removeClass('vH');
			});
			This.but_right.click(function(){
				$('.img_a .em2').addClass('vH').siblings('em').removeClass('vH');
				
			})
			
		},
		Pro:function(){
			This=this;
			$.ajax({
				type : 'POST',
				async : true,
				url : "/yiquan/searchwork",
				data:{
					workId:H.mark.getWorkId
				},
				dataType : "json",
				success : function(data) {

					H.mark.$workId=data.workId;
					if(data.AuthorSize==0){
						data.AuthorSize="S"
					}
					if(data.AuthorSize==1){
						data.AuthorSize="M"
					}
					if(data.AuthorSize==2){
						data.AuthorSize="L"
					}
					if(data.AuthorSize==3){
						data.AuthorSize='XL'
					}


					var data_Url="http://"+window.location.host+data.workImageSFront;
					$("header h1").html(data.nickname+"的design");
					$('.number').text(data.workId);
					$('.vote').text(data.vote);

					$('.size').text(data.AuthorSize);
					$('.ranking').text(data.top);

					if(data.AuthorColors==0) IndexImg=7;
					if(data.AuthorColors==1) IndexImg=3;
					if(data.AuthorColors==2) IndexImg=5;
					if(data.AuthorColors==3) IndexImg=1;

					$('.product em.em1>img').attr('src',"/static/campaigns/yiquan/mobile/img/yifu/"+IndexImg+".png");
					$('.product em.em2>img').attr('src',"/static/campaigns/yiquan/mobile/img/yifu/"+(IndexImg+1)+".png");

					$('.product em.em1 i img').attr('src',data.workImageSFront);
					$('.product em.em2 i img').attr('src',data.workImageSBack);
					//打印码不一定有  后期要做容错处理
					$('.dym').html('打印码'+data.AuthorCode);
					$('.buts_2').click(function(){
						window.location.href="wx-product.html?workId="+data.workId;
					})

					This.shareFun(data.workId)//分享
				},
				error:function(jqXHR){
					alert("数据请求失败，请稍后再试");
					return false;
				}
			});
		},
		Click:function(){
			This=this;
			This.but_1.click(function(){
				This.Tip_1('makeSuccess6')
			})
			This.voteA.click(function(){
				This.vote();
			});
			$('.qrsc').click(function(){
				This.Tip_1('weMake2');
			});
			$('.buts_2').click(function(){
        		window.location.href='wx-product.html?workId='+H.mark.getWorkId;
        	});

        	$('.qrscEnd').click(function(){


        		$.ajax({
						type : 'POST',
						async : true,
						timeout:2000,
						url : "/yiquan/finishWork",
						data:{
							workId:H.mark.getWorkId
						},
						dataType : "json",
						success : function(data) {
							if(data.result_code){
								alert(data.msg);
							}else{
								window.location.href="wx-makeSuccess.html?workId="+data.workId;
							}
						},
						error:function(jqXHR,textStatus){
							if(textStatus=="timeout"){
		                        alert("请求超时，请重试");
		                        return false;
		                    }
							alert("数据请求失败，请稍后再试");
							return false;
						}
					});



        	})
		},
		vote:function(){
			var This=this;
			$.ajax({
				type : 'POST',
				async : true,
				url : "vote",
				data:{
					workId:H.mark.$workId
				},
				dataType : "json",
				success : function(data) {
					This.Tip('otherProduct1');
					$('.vote').html( parseInt($('.vote').html())+1 )
				},
				error:function(jqXHR){
					alert("您今天投票次数已经用完");
					return false;
				}
			});



		},
		Tip:function(imgName){
			var t = simpleTpl();
         		t._('<div class="dialog_img otherProduct_dialog">')
						._('<div class="make_dialog">')
							._('<em><img src="/static/campaigns/yiquan/mobile/img/'+imgName+'.png"/></em>')
						._('</div>')
				._('</div>')

        	$('body').append(t.toString());
        	$('.dialog_img').addClass('active');
        	var Time=setTimeout(function(){
        		$('.dialog_img').remove()
        	},3000);

        	$('.dialog_img').bind("click",function(){
				$('.dialog_img').remove();
				clearTimeout(Time);
			})

		},
		Tip_1:function(imgName){
			var t = simpleTpl();
         		t._('<div class="dialog_img">')
						._('<div class="make_dialog">')
							._('<em><img src="/static/campaigns/yiquan/mobile/img/'+imgName+'.png"/></em>')
						._('</div>')
				._('</div>')

        	$('body').append(t.toString());
        	$('.dialog_img').addClass('active');
        	var Time=setTimeout(function(){
        		$('.dialog_img').remove()
        	},3000);

        	$('.dialog_img').bind("click",function(){
				$('.dialog_img').remove();
				clearTimeout(Time);
			})


		},
		shareFun:function(workId){


	var shareUpdate = function () {
		var	IndexUrl=window.location.href;
		$.ajax({
				type: "POST",
				url: "http://fanta.kuh5.net/yiquan/mobile/mobile_share",
				data: {
					url:IndexUrl,
					workId : workId
				},
				async: !0,
				dataType: "json",
				success: function(a) {
				},
				error: function(a, b) {}
		})
	}

	var WX_share=function(){

			var  TT='我的+Chao T，潮不潮你说了算！';
			var ImgUrl="http://fanta.kuh5.net/static/campaigns/yiquan/mobile/img/share.png";
			var Desc='+Chao T我创，投我一票，带你玩的就是+Chao！';
			var	IndexUrl=window.location.href;
			var Url="http://fanta.kuh5.net/yiquan/wx-otherProduct.html?workId="+workId;
			$.ajax({
				type: "POST",
				url: "http://fanta.kuh5.net/yiquan/getSignPackage",
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
									shareUpdate()
								}
							});
							wx.onMenuShareAppMessage({
								title: TT,
								desc: Desc,
								link: Url,
								imgUrl:ImgUrl,
								success:function(){
									shareUpdate()
								}
							});
							wx.onMenuShareQQ({
								title: TT,
								desc: Desc,
								link: Url,
								imgUrl: ImgUrl,
								success:function(){
									shareUpdate()
								}
							});
							wx.onMenuShareWeibo({
								title: TT,
								desc: Desc,
								link: Url,
								imgUrl: ImgUrl,
								success:function(){
									shareUpdate()
								}
							});
							wx.onMenuShareQZone({
								title: TT,
								desc: Desc,
								link: Url,
								imgUrl: ImgUrl,
								success:function(){
									shareUpdate()
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


		}
		
	};
})(Zepto);

$(function() {
	H.mark.init();
});