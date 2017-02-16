var aniTrue = true;
	var showTips = function(word, pos, timer) {
	if (aniTrue) {
		aniTrue = false;
		var pos = pos || '2',
		timer = timer || 1500;
		$('body').append('<div class="tips none"></div>');
		$('.tips').css({
			'position': 'fixed' ,
			'max-width': '80%' ,
			'top': '60%' ,
			'left': '50%' ,
			'z-index': '99999999' ,
			'color': 'rgb(255, 255, 255)' ,
			'padding': '20px 10px' ,
			'border-radius': '5px' ,
			'margin-left': '-120px' ,
			'background': 'rgba(0, 0, 0, 0.8)' ,
			'text-align': 'center'
		});
		$('.tips').html(word);
		var winW = $(window).width(),
			winH = $(window).height();
		$('.tips').removeClass('none').css('opacity', '0');
		var tipsW = $('.tips').width(),
			tipsH = $('.tips').height();
		$('.tips').css({'margin-left': -tipsW/2,'top':(winH - tipsH)/(pos - 0.2)}).removeClass('none');
		$('.tips').animate({
			'opacity': '1',
			'top': (winH - tipsH)/pos}, 300, function() {
				setTimeout(function() {
					$('.tips').animate({'opacity':'0'}, 300, function() {
						$('.tips').addClass('none').css('top', (winH - tipsH)/(pos - 0.2));
					});
				}, timer);
				setTimeout(function() {
					$('.tips').remove();
					aniTrue = true;
				}, timer + 350);
		});
	};
};

var simpleTpl = function( tpl ) {
    tpl = $.isArray( tpl ) ? tpl.join( '' ) : (tpl || '');

    return {
        store: tpl,
        _: function() {
            var me = this;
            $.each( arguments, function( index, value ) {
                me.store += value;
            } );
            return this;
        },
        toString: function() {
            return this.store;
        }
    };
};
//首次打开
table.controller('Index',['$scope','$http','$location','$rootScope',function($scope,$http,$location,$rootScope){
	var Promise=$rootScope.checkFirst();
		Promise.then(function(){
			if(sessionStorage.getItem('checkfirst')=='true'){
				//$location.url('/successIndex');
				return false;
			}
			setTimeout(function(){
				document.querySelector('#index_wrap').style.opacity='1';
			},100)
			var main_wrap=document.getElementById('main_wrap');
			var envelope=document.querySelector('#envelope');
			var envelope1=document.querySelector('#envelope1');
			var Enve=document.querySelector('#envelope1');
			var share=document.querySelector('#share');
			$scope.list={
				Shake:function(){
					main_wrap.className='mainAnim';
					envelope.className='envelope';
					envelope1.className='envelope';
					share.className='share';
				},
			}
			
			//查当前总步数与总金额
		$http.get('main').success(function(response){ // 查件总金币与总步数
			$rootScope.totalStep=response.count;
			//$rootScope.totalStep=5000001;
			$rootScope.totalMoney=response.money;
			sessionStorage.setItem('totalStep',$rootScope.totalStep);
			if($rootScope.totalStep>5000000 && $rootScope.totalStep<=60000000){
				var conentDiv = document.createElement("link");
				conentDiv.href='/static/campaigns/ticai/mobile/css/index_1.css';
				conentDiv.rel='stylesheet';
				conentDiv.id='css_style';
				document.body.appendChild(conentDiv);
			}else if($rootScope.totalStep>60000000){
				var conentDiv = document.createElement("link");
				conentDiv.href='/static/campaigns/ticai/mobile/css/index_2.css';
				conentDiv.rel='stylesheet';
				conentDiv.id='css_style';
				document.body.appendChild(conentDiv);
			}
		})
		//判断上传时间限制
		var day=new Date();
		var Month=day.getMonth()+1;
		var dayStr=day.getDate().toString();
		if(dayStr.length==1){
			dayStr='0'+dayStr;
		}
		var xianzhi=Month+''+dayStr;
		if(xianzhi>1115){
			$('.donation').css({'background':"url('/static/campaigns/ticai/mobile/image/1/onUpload.png')",'background-size':"contain"})
		}
		if(xianzhi==1025){
			$('.donation').css({'background':"url('/static/campaigns/ticai/mobile/image/1/onUpload.png')",'background-size':"contain"})
		}
		var Hours=new Date().getHours();
		if(Hours>8 && Hours<24){
		}else{
			$('.donation').css({'background':"url('/static/campaigns/ticai/mobile/image/1/onUpload.png')",'background-size':"contain"})
		}
		$scope.uploadHtml=function(){
			if(xianzhi==1025){
				showTips('活动尚未开始');
				return false;
			}
			if(xianzhi>1115){
				showTips('活动已经结束');
				return false;
			}
			if(Hours>8 && Hours<24){
				window.location.href='about.html';
			}else{
				showTips('9:00开始,过会儿再来');
		
			}
		}
		
		})
		
	
}])
//上传之后打开首页
table.controller('successIndex',['$rootScope','$scope','$http',function($rootScope,$scope,$http){
	
	var Promise=$rootScope.checkFirst();
	Promise.then(function(){
		
	var main_wrap=document.getElementById('main_wrap');
	var envelope=document.querySelector('#envelope');
	var envelope1=document.querySelector('#envelope1');
	var Enve=document.querySelector('#envelope1');
	var share=document.querySelector('#share');
	$scope.list={
		Shake:function(){
			main_wrap.className='mainAnim';
			envelope.className='envelope';
			envelope1.className='envelope';
			share.className='share'
		},
	}
	$http.get('fetch').success(function(response){  //查看个人步数与金币
		$scope.counts=response.count;
		$scope.money=response.money;
		$scope.count=parseInt(sessionStorage.getItem('dangqiwalk'));
		if($scope.count>=0 && $scope.count<3000){
			$scope.Pngname=1;
		}else if($scope.count>=3000 && $scope.count<=3999){
			$scope.Pngname=2;
		}else if($scope.count>=4000 && $scope.count<=6999){
			$scope.Pngname=3;
		}else if($scope.count>=7000 && $scope.count<=9999){
			$scope.Pngname=4;
		}
		else if($scope.count>=10000 && $scope.count<=19999){
			$scope.Pngname=5;
		}
		else if($scope.count>=20000){
			$scope.Pngname=6;
		}
		$scope.Share();
	})
	//分享
	$scope.Share=function(){
			var Walk=sessionStorage.getItem('dangqiwalk');
			var Openid=sessionStorage.getItem('Openid');
			var imgName,Desc;
			var Url="http://fanta.kuh5.net/ticai/shareIndex?Openid="+Openid;
			if(Walk>=0 && Walk<3000){
				imgName=1;
				Desc='今天我走路消耗的热量太少啦，明天多走点吧！';
			}else if(Walk>=3000 && Walk<=3999){
				imgName=2;
				Desc='今天我走路消耗的热量大约为1瓶碳酸饮料,你也来试试吧！';
			}else if(Walk>=4000 && Walk<=6999){
				imgName=3;
				Desc='今天我走路消耗的热量大约为1个巧克力蛋糕,你也来试试吧！';
			}else if(Walk>=7000 && Walk<=9999){
				imgName=4;
				Desc='今天我走路消耗的热量大约为1个巨无霸汉堡,你也来试试吧！';
			}
			else if(Walk>=10000 && Walk<=19999){
				imgName=5;
				Desc='今天我走路消耗的热量大约为1碗桶装方便面,你也来试试吧！';
			}
			else if(Walk>=20000){
				imgName=6;
				Desc='今天我走路消耗的热量大约为1大块披萨,你也来试试吧！';
			}else{
				imgName=7;
				Url="http://fanta.kuh5.net/ticai/index";
				Desc='江苏体彩爱行走第二季，向不可能说“步”！'
			}
			var	IndexUrl=window.location.href;	
			var  TT='体彩爱行走';
			var ImgUrl='http://fanta.kuh5.net/static/campaigns/ticai/mobile/image/share/'+imgName+'.png';
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
								title:Desc,
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

	}
	//分享结束
	
	
	})
	
}]);

//列表
table.controller('List',['$scope','$http','$timeout',function($scope,$http,$timeout){
	//下拉刷新
	var myScroll;
	myScroll = new IScroll('#wrapper', { 
	  mouseWheel: false,  //是否监听鼠标滚轮事件
	  bounceTime:600,    //弹力动画持续的毫秒数
	  probeType: 3
	 });
	 myScroll.on('scrollStart', function(){
	 	//console.log("开始");
	 	});
	 var  handle=0;
	 myScroll.on('scroll', function(){
	 	
	 	if (this.y > 5) {
		   //下拉刷新效果  
		   handle=1;
//			   if(this.y>20){
//			   	document.getElementById('request').style.opacity=1;
//			   }else{
//			   	document.getElementById('request').style.opacity=0;
//			   }
		  } else if (this.y < (this.maxScrollY - 5)) {
		   //上拉刷新效果  
		 	 handle=2;
		 	 if(this.maxScrollY-this.y>20){
		 	 	document.getElementById('response').style.opacity=1;
		 	 }else{
		 	 	document.getElementById('response').style.opacity=0;
		 	 }
		  };
	 }); 
	 var pageSNum=1;
	 var nowPage=1;
	 $scope.total=0;
	 myScroll.on('scrollEnd', function(){
	 	if(handle==1){
		   //下拉刷新处理
		   downrefresh();
		   handle=0;//重设为0，改为无状态
		  }else if(handle==2){
		   //上拉刷新处理
		   handle=0;//重设为0，改为无状态;
		   nowPage++;
		   if(nowPage>$scope.total){
		   	return false;
		   }
		   upajaxload(nowPage);
		  }else{handle=0;};  
	 });
	 
	 wrapper.ontouchstart=function(e){
	 	var startX=e.touches[0].clientX;
	 	var moveX=0,difference=0;
	 	this.ontouchmove=function(e){
	 		moveX=e.touches[0].clientX;
	 		difference=Math.abs(startX-moveX);
	 		if(difference<20){
	 			box.ontouchmove=null;
				box.ontouchend=null;
	 		console.log(difference)
	 		}else{
	 			//This.Swip();
	 			console.log(123)
	 		}
	 	}
	 }
	function downrefresh(){//刷新处理
	  //console.log("下拉");
	  
	  myScroll.refresh();
	  
	 };
	 function upajaxload(nowPage){//加载处理
	  console.log("上拉");
	  //dream(pageSNum);
	  jiazai(nowPage);
	  myScroll.refresh();
	 };
	//下拉刷新完结
	$scope.Active=true;
	$scope.listBox1=function(){
		$scope.Active=true;
	}
	$scope.listBox2=function(){
		$scope.Active=false;
	}
	// 排行列表查询
	
	$scope.usrprices=true;
	$scope.walkCount=[];
	var arr=[],arr1=[];
	var j=0;
	function jiazai(nowPage){
		var Option={
			now_page:nowPage||1,
			page_rows:'8'
		}
		console.log(Option.now_page)
		$http({
			method:'GET',
			url:'workcount',
			params:Option,
		}).success(function(response){
		//alert(JSON.stringify(response))
			$scope.data=response;
			var t=simpleTpl();
			try{
				for(var i=0;i<response.walkCount.length;i++){
					
//					var valLength=response.walkCount[i].user.toString().length;
//					var str='0';
//					for(var k=0;k<(6-valLength-1);k++){
//						str+='0';
//					}
//					response.walkCount[i].user=str+response.walkCount[i].user;
					var info=response.walkCount[i].info;
					if(info==null){
						info='无'
					}else{
						
					info=info.slice(0,3)+"*****"+info.slice(info.length-3,info.length)
					}
					
					j++;
					t._('<li>')
						._('<span>')
						if(j>3){
							t._('<em>'+j+'</em>')
						}else{
							t._('<img src="/static/campaigns/ticai/mobile/image/1/a'+(i+1)+'.png"/>')
						}
						t._(' </span>')
						._('<span><img src="/static/campaigns/ticai/mobile/image/1/c'+(i+1)+'.png"/></span>')
						._('<span>'+info+'</span>')
						._('<span>'+response.walkCount[i].walk+'<i>步</i></span>')
					._('</li>');
				}
			}catch(e){
				//t._('<p style="text-align: center;">'+response.result_msg+'</p>');
				t._('<p style="text-align: center;">您的步数及排名将于次日14:00前公布</p>');
				//TODO handle the exception
			}
			$scope.result_code=false;
			if(response.result_code==0){
				$scope.result_code=true;
			}
			$('#wrapper ul').append(t.toString());
			if($scope.data.isend==0){
				if($scope.data.isUser==0){
					$scope.Name=localStorage.getItem('name');
					$scope.Phone=localStorage.getItem('Phone');
					if(localStorage.getItem('name') && localStorage.getItem('Phone')){
						$scope.disAb=true;
					}
					$scope.usrprices=false;
				}
			}
			
			$scope.total= Math.ceil(response.total_count/Option.page_rows);
			myScroll.refresh();
//			console.log($scope.total)
			$timeout(function(){
				myScroll.refresh();
			},2000)
		})
	}
	
	jiazai();
	
	$scope.Reset=function(){
		$scope.disAb=false;
	}
	var ph=/^1(3|4|5|7|8)\d{9}$/;
	$scope.Submit=function(){
		if($scope.Name==undefined){
			showTips('请填写姓名');
			return false;
		}
		if($scope.Phone==undefined){
			showTips('请填写手机号');
			return false;
		}
		
		if(!ph.test($scope.Phone)){
			showTips('请填写正确的手机号');
			return false;
		}
		var str='手机号 '+$scope.Phone+' 姓名 '+$scope.Name;
        var data={usrinfo:str};
        $http({
        	method:"get",
        	url:'usrprices',
        	params:data,
        }).success(function(resopnse){
        	showTips('提交成功');
        	$timeout(function(){
				$scope.usrprices=true;
			},1000)
        })
	}
	$http.get('myDonate').success(function(response){ // 我的步数每周查询
		var Day=response.day;
		$scope.day=Day;
		$scope.noCheck=response.no_check;
		$scope.week=response.week;
		if($scope.week==[]){
			$scope.week=[1];
		}
		//alert(JSON.stringify(response))
	});
	setTimeout(function(){
		document.querySelector('#list').style.opacity='1';
	},100)
}])

// 奖品
table.controller('Prize',['$rootScope','$scope','$http',function($rootScope,$scope,$http){
	if(localStorage.getItem('priceLength')){
		$scope.priceLength=false;
	}else{
		$scope.priceLength=true;
	}
	setTimeout(function(){
		document.querySelector('#prize').style.opacity='1';
	},100)
	$scope.showbox=false;
	var price_new=document.querySelector('#price_new');
	var Time=new Date();
	var getMonth=Time.getMonth()+1;
	Month=getMonth<10?('0'+getMonth):getMonth;
	var str=Time.getFullYear()+"-"+Month+"-"+Time.getDate();
	$scope.Time=str;
	$http.get('getprice').success(function(response){  //查看奖品接口
		var data=response.priceinfo;
		if(data.length==0){
			$scope.priceLength=true;
		}else{
			$scope.priceLength=false;
			localStorage.setItem('priceLength','true')
			//去掉数字提示
			$scope.pricelist=data;
			price_new.innerHTML='';
			price_new.className='none';
			$scope.Show=function(index){
				console.log(123)
				$scope.IndexData=data[index];
				$scope.showbox=true;
			}
			$scope.showClose=function(){
				$scope.showbox=false;
			}
		}
	})
}])


//线下报名
table.controller('SignUp',["$scope","$http",'$timeout',function($scope,$http,$timeout){
	$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
	$scope.activeText=false;
	$scope.sm=false;
	if(localStorage.getItem('activetext1_new_1')){
		$scope.cjName=localStorage.getItem('name_new_1');
		$scope.cjPhone=localStorage.getItem('Phone_new_1');
		document.querySelector('#cj_1').setAttribute('src','/static/campaigns/ticai/mobile/image/10-12.png');
		$scope.disaBled=true;
		//return false;
	}
	//var ph=/^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$/;
	var ph=/^1(3|4|5|7|8)\d{9}$/;
	$scope.Submit=function(){
		//console.log(typeof $scope.Name);
		if($scope.disaBled){
			showTips('已报名')
			return false;
		}
		if($scope.Name==undefined){
			showTips('请填写姓名');
			return false;
		}
		if($scope.Phone==undefined){
			showTips('请填写联系方式');
			return false;
		}
		if(!ph.test($scope.Phone)){
			showTips('请填写正确的手机号');
			return false;
		}
		var str='手机号 '+$scope.Phone+' 姓名 '+$scope.Name;
        var data={usrinfo:str};
        //alert(JSON.stringify(data))
        $http({                     //线下报名接口
			method:'POST',
			url:"signin",
			data:$.param(data),
			async:false,
			dataType:'json'
		}).success(function(re){
			//alert(JSON.stringify(re))
			$scope.activeText=true;
			$scope.disaBled=true;
			document.querySelector('#cj_1').setAttribute('src','/static/campaigns/ticai/mobile/image/10-12.png')
			//console.log($scope.activeText)
			localStorage.setItem('name_new_1',$scope.Name);
			localStorage.setItem('Phone_new_1',$scope.Phone);
			$scope.cjName=localStorage.getItem('name_new_1');
			$scope.cjPhone=localStorage.getItem('Phone_new_1');
			$timeout(function(){
				$scope.activeText=false;
				localStorage.setItem('activetext1_new_1',$scope.Phone);
			},1800)
		})
	}
	$scope.shuom=function(){
		$scope.sm=true;
	}
	$scope.shuomClose=function(){
		$scope.sm=false;
	}
	
	setTimeout(function(){
		document.querySelector('#sign_up').style.opacity='1';
	},100)
}])
//活动说明
//table.controller('Explain',['$scope',function($scope){
//	
//}])
//
table.run(['$rootScope','$location','$http','$q',function($rootScope,$location,$http,$q){
		var deferred = $q.defer();
		var one=0;
		$rootScope.checkFirst=function(){
			if(one==0){
				$http.get('checkfirst').success(function(response){
					if(response.result_code==1){  //1上传了
						sessionStorage.setItem('checkfirst','true');
						document.querySelector('#index_a').setAttribute('href','#/successIndex');
						sessionStorage.setItem('dangqiwalk',response.walk);
						sessionStorage.setItem('Openid',response.id);
						$location.url('/successIndex');
					}else{
						$location.url('/');
					}
					deferred.resolve('1');
					++one;
				})
			}
			return deferred.promise;
		}
	var price_new=document.querySelector('#price_new')
	$http.get('priCount').success(function(response){  //查看是否有未查看的奖品列表
		if(response.price_new){
			price_new.innerHTML=response.price_new;
			price_new.className='';
		}
	})
	
	//判断当日有没有上传图片
	
	
	//$routeChangeSuccess,$routeChangeStart
	//$locationChangeSuccess,$locationChangeStart
	 var locationChangeStartOff = $rootScope.$on('$routeChangeSuccess', function(){
		 var main_footer=document.querySelector('#main_footer');
		 var aA=main_footer.querySelectorAll('a');
		 
		 for(var i=0;i<aA.length;i++){
		 	aA[i].className='';
		 }
		 var Url=$location.path();
		console.log(Url)
		 try{
		 	var thisNode=document.querySelector('#css_style');
		 	if(thisNode && Url!='/'){
		 		thisNode.parentNode.removeChild(thisNode);
		 		if(thisNode){
		 			setTimeout(function(){
		 				//thisNode.parentNode.removeChild(thisNode);
		 			},30)
		 		}
		 	}
		 }catch(e){
		 	
		 }
		 
		 
	 	switch (Url){
	 		case '/':
	 			aA[0].className='active';
	 			break;
	 		case '/successIndex':
	 			aA[0].className='active'
	 			break;
	 		case '/list':
	 			aA[1].className='active'
	 			break;
	 		case '/prize':
	 			aA[2].className='active'
	 			break;
	 		case '/signUp':
	 			aA[3].className='active'
	 			break;
	 		case '/explain':
	 			aA[4].className='active'
	 			break;	
	 		default:
	 			aA[0].className='active'
	 			break;
	 	}
	 });
}])






$(function(){
	var main_wrap=document.getElementById('main_wrap');
	var envelope=document.querySelector('#envelope');
	var envelope1=document.querySelector('#envelope1');
	var Enve=document.querySelector('#Enve');
	var share=document.querySelector('#share');
	setTimeout(function(){
		main_wrap.style.webkitTransition='all 1s';
		envelope.style.webkitTransition='all 1s';
		envelope1.style.webkitTransition='all 1s';
	},500)
	Enve.onclick=function(){
		main_wrap.className='';
		envelope.className='';
		envelope1.className='';
		share.className='none';
	}
})



