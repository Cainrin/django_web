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
table.controller('Index',['$scope','$http','$location',function($scope,$http,$location){
	var main_wrap=document.getElementById('main_wrap');
	var envelope=document.querySelector('#envelope');
	var envelope1=document.querySelector('#envelope1');
	var Enve=document.querySelector('#envelope1');
	$scope.list={
		Shake:function(){
			main_wrap.className='mainAnim';
			envelope.className='envelope';
			envelope1.className='envelope';
		},
	}
	if(sessionStorage.getItem('checkfirst')=='true'){
		$location.url('/successIndex');
	}
	
	//查当前总步数与总金额
	$http.get('main').success(function(response){ // 查件总金币与总步数
		$scope.totalStep=response.count;
		$scope.totalMoney=response.money;
	})
}])
//上传之后打开首页
table.controller('successIndex',['$scope','$http',function($scope,$http){
	var main_wrap=document.getElementById('main_wrap');
	var envelope=document.querySelector('#envelope');
	var envelope1=document.querySelector('#envelope1');
	var Enve=document.querySelector('#envelope1');
	$scope.list={
		Shake:function(){
			main_wrap.className='mainAnim';
			envelope.className='envelope';
			envelope1.className='envelope';
		},
	}
	$http.get('fetch').success(function(response){  //查看个人步数与金币
		console.log(response)
		$scope.count=response.count;
		$scope.money=response.money;
		$scope.count=parseInt(sessionStorage.getItem('dangqiwalk'));
		console.log($scope.count)
		if($scope.count>0 && $scope.count<3000){
			$scope.Pngname=1;
		}else if($scope.count>=3000 && $scope.count<=3999){
			$scope.Pngname=2;
		}else if($scope.count>=4000 && $scope.count<=6999){
			$scope.Pngname=3;
		}else if($scope.count>=7000 && $scope.count<=9999){
			$scope.Pngname=4;
		}
		else if($scope.count>=10000 && $scope.count<=1999){
			$scope.Pngname=5;
		}
		else if($scope.count>=20000){
			$scope.Pngname=6;
		}
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
	var j=1;
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
			$scope.data=response;
			var t=simpleTpl();
			//$scope.walkCount=$scope.walkCount.concat(response.walkCount)
			try{
				for(var i=0;i<response.walkCount.length;i++){
					j++;
					t._('<li>')
						._('<span><em ng-if='+(i>2)+'>'+j+'</em> <img ng-if='+(i<=2)+' ng-src="image/1/a'+(i+1)+'.png"/></span>')
						._('<span><img src="image/1/c'+i+'.png"/></span>')
						._('<span>'+response.walkCount[i].user+'</span>')
						._('<span>'+response.walkCount[i].walk+'<i>步</i></span>')
					._('</li>');
				}
			}catch(e){
				t._('<p style="text-align: center;">'+response.result_msg+'</p>');
				$scope.result_code=1;
				if(response.result_code=1){
					$scope.result_code=false;
				}
				//TODO handle the exception
			}
			
			$('#wrapper ul').append(t.toString());
			
			if($scope.data.isUser==1){
				$scope.Name=localStorage.getItem('name');
				$scope.Phone=localStorage.getItem('Phone');
				$scope.disAb=true;
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
	
	$scope.Submit=function(){
		var str='手机号 '+$scope.Phone+' 姓名 '+$scope.Name;
        var data={usrinfo:str};
        $http.get('usrprices').success(function(resopnse){
        	console.log(resopnse);
        	$timeout(function(){
				$scope.usrprices=false;
			},1000)
        })
	}
	$http.get('myDonate').success(function(response){ // 我的步数每周查询
		var Day=response.day;
		$scope.day=Day;
		$scope.week=response.week;
		if($scope.week==[]){
			$scope.week=[1];
		}
	});
}])

// 奖品
table.controller('Prize',['$rootScope','$scope','$http',function($rootScope,$scope,$http){
	if(localStorage.getItem('priceLength')){
		$scope.priceLength=false;
	}else{
		$scope.priceLength=true;
	}
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
	$scope.activeText=false;
	$scope.sm=false;
	if(localStorage.getItem('activetext1')){
		$scope.cjName=localStorage.getItem('name');
		$scope.cjPhone=localStorage.getItem('Phone');
		$scope.disaBled=true;
		//return false;
	}
	$scope.Submit=function(){
		//console.log(typeof $scope.Name);
		if($scope.disaBled){
			showTips('已报名')
			return false;
		}
		if($scope.Name==undefined){
			showTips('请填写姓名');
			return false;
		}if($scope.Phone==undefined){
			showTips('请填写联系方式');
			return false;
		}
		var str='手机号 '+$scope.Phone+' 姓名 '+$scope.Name;
        var data={usrinfo:str};
        $http({                     //线下报名接口
			method:'POST',
			url:"signin",
			data:$.param(data),
			async:false,
			dataType:'json'
		}).success(function(){
			$scope.activeText=true;
			$scope.disaBled=true;
			console.log($scope.activeText)
			localStorage.setItem('name',$scope.Name);
			localStorage.setItem('Phone',$scope.Phone);
			$scope.cjName=localStorage.getItem('name');
			$scope.cjPhone=localStorage.getItem('Phone');
			$timeout(function(){
				$scope.activeText=false;
				localStorage.setItem('activetext1',$scope.Phone);
			},1000)
		})
        
	}
	$scope.shuom=function(){
		$scope.sm=true;
	}
	$scope.shuomClose=function(){
		$scope.sm=false;
	}
	
	
}])

//活动说明
//table.controller('Explain',['$scope',function($scope){
//	
//}])
//
table.run(['$rootScope','$location','$http',function($rootScope,$location,$http){
	
	var price_new=document.querySelector('#price_new')
	$http.get('priCount').success(function(response){  //查看是否有未查看的奖品列表
		if(response.price_new){
			price_new.innerHTML=response.price_new;
			price_new.className='';
		}
	})
	
	//判断当日有没有上传图片
	$http.get('checkfirst').success(function(response){
		if(response.result_code==1){  //1上传了
			sessionStorage.setItem('checkfirst','true');
			document.querySelector('#index_a').setAttribute('href','#/successIndex');
			sessionStorage.setItem('dangqiwalk',response.walk);
			sessionStorage.setItem('Openid',response.id);
		}
	})
	
	
	
	//$routeChangeSuccess,$routeChangeStart
	//$locationChangeSuccess,$locationChangeStart
	 var locationChangeStartOff = $rootScope.$on('$routeChangeSuccess', function(){
		 var main_footer=document.querySelector('#main_footer');
		 var aA=main_footer.querySelectorAll('a');
		 for(var i=0;i<aA.length;i++){
		 	aA[i].className='';
		 }
		 var Url=$location.path();
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
	setTimeout(function(){
		main_wrap.style.webkitTransition='all 1s';
		envelope.style.webkitTransition='all 1s';
		envelope1.style.webkitTransition='all 1s';
	},500)
	Enve.onclick=function(){
		main_wrap.className='';
		envelope.className='';
		envelope1.className='';
	}
})



