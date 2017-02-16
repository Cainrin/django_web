
var ticai=angular.module('myApp',[]);

ticai.directive('nav',function(){
	return{
		restrict:'E',
		templateUrl:'/static/campaigns/ticai/pc/view/nav.html',
		replace:true,
		scope:{
			myId:'@',
			myData:"=",
			myPath:'='
		},
		link:function(s,e,a){
		
			e.on('click','li a',function(){
				$(this).addClass('active').parent('li').siblings('li').find('a').removeClass('active');
			});
		}
	}
})
ticai.controller('listTitle',['$scope','$location',function($scope,$location){
	$scope.Title=[
		{title:'活动数据',route:'/'},
		{title:'用户数据',route:'user'},
		{title:'实物奖品',route:'award'},
		{title:'线下活动',route:'offline'},
		{title:'奖券发布',route:'draw'},
		{title:'查看PV-UV',route:'progressive'},
		{title:'奖券信息',route:'message'},
		{title:'排行查看',route:'rank'}
	];
	$scope.Path=$location.path().slice(1);
	
}])
//右侧路由控制
var table=angular.module('myTable',['ngRoute','ngSanitize','tm.pagination']);
table.config(function($routeProvider){
	$routeProvider.when('/',{
		templateUrl:'/static/campaigns/ticai/pc/view/active.html',
		controller:'Active'
	}).when('/user',{
		templateUrl:'/static/campaigns/ticai/pc/view/user.html',
		controller:'User'
	}).when('/award',{
		templateUrl:'/static/campaigns/ticai/pc/view/award.html',
		controller:'Award'
	}).when('/offline',{
		templateUrl:'/static/campaigns/ticai/pc/view/offline.html',
		controller:'Offline'
	}).when('/draw',{
		templateUrl:'/static/campaigns/ticai/pc/view/draw.html',
		controller:'Draw'
	}).when('/progressive',{
		templateUrl:'/static/campaigns/ticai/pc/view/progressive.html',
		controller:'Progressive'
	})
	.when('/actived/:id',{
		templateUrl:'/static/campaigns/ticai/pc/view/active.html',
		controller:'UserFind'
	}).when('/message',{
		templateUrl:'/static/campaigns/ticai/pc/view/message.html',
		controller:'Message'
	})
	.when('/rank',{
		templateUrl:'/static/campaigns/ticai/pc/view/rank.html',
		controller:'Rank'
	})
	.when('/Rank/:id/:countType',{
		templateUrl:'/static/campaigns/ticai/pc/view/rankId.html',
		controller:'RankId'
	})
	.otherwise({
		redirectTo:'/'
	})
})
//奖券信息
table.controller('Message',['$scope','$http','$rootScope','BusinessService','PostService',function($scope,$http,$rootScope,BusinessService,PostService){
		$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
	//日历插件调用
	var d = new Date();
	//var str = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+(d.getDate()-1);
	$scope.timestart='2016-07-1';
	$scope.timend=d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();;
	var dateRange = new pickerDateRange('date_demo3', {
		//aRecent7Days : 'aRecent7DaysDemo3', //最近7天
		isTodayValid : false,
		startDate : '2016-07-1',
		endDate : $scope.timend,
		//needCompare : true,
		//isSingleDay : true,
		//shortOpr : true,
		defaultText : ' 至 ',
		inputTrigger : 'input_trigger_demo3',
		theme : 'ta',
		success : function(obj) {
			//$("#dCon_demo3").html('开始时间 : ' + obj.startDate + '<br/>结束时间 : ' + obj.endDate);
			$scope.timestart=obj.startDate;
			$scope.timend=obj.endDate;
			
		}
	});
	// 日历插件结束
	//配置分页基本参数
    $scope.paginationConf = {
        currentPage: 1,
        itemsPerPage: 5
    };
	//分页功能；
	$scope.suchchoice='time';
 	$scope.GetAllEmployee = function (num) {
        var postData = {
        	startime:$scope.timestart,
	        endtime:$scope.timend,
            now_page: $scope.paginationConf.currentPage,
            page_rows: $scope.paginationConf.itemsPerPage,
            excel:''
//          suchchoice:num==undefined?'time':num,
//          type:'0'
        }
        BusinessService.list('priceInfo',postData).success(function (response) {
        	console.log(response)
            $scope.paginationConf.totalItems = response.total_count;
           	$scope.priceList=response.list
            
        });
    }
	
	//发送日奖品
	$scope.sendPrize=function(){
		$.ajax({
		    type: "POST",
		    url: 'sendPrize',
		    data: {id:$routeParams.id},
		    success: function(response) {
		        console.log(response);
		        if(response.result_code==0){
		        	alert('发放成功');
		        }
		        
		    }
		});
	}
	//发送周奖品
	$scope.accessToken=function(){
		$.ajax({
		    type: "POST",
		    url: 'accessToken',
		    data: {id:$routeParams.id},
		    success: function(response) {
		        console.log(response);
		        if(response.result_code==0){
		        	alert('发放成功');
		        }
		    }
		});
	}
	
    

    /***************************************************************
    	当页码和页面记录数发生变化时监控后台查询
    	如果把currentPage和itemsPerPage分开监控的话则会触发两次后台事件。 
    ***************************************************************/
    var unWatch=$scope.$watch('paginationConf.currentPage+paginationConf.itemsPerPage'+$scope.suchchoice, $scope.GetAllEmployee);
    
    //搜索
    $scope.extype=0;
    $scope.Search=function(){
    	unWatch();
    	function SeaFun() {
    		currentPage=$scope.paginationConf.currentPage<=0?'1':$scope.paginationConf.currentPage
	    	var postSearch = {
	            now_page: currentPage,
	            page_rows: $scope.paginationConf.itemsPerPage,
	            id:$scope.keyValue==''||$scope.keyValue==undefined?'None':$scope.keyValue,
	            startime:$scope.timestart,
	            endtime:$scope.timend,
	            excel:''
	            //type:$scope.suchchoice,
	            //extype:0,
	        }
	    	BusinessService.list('priceInfo',postSearch).success(function (response) {
	    		console.log(response)
	    		 $scope.paginationConf.totalItems = response.total_count;
           		$scope.priceList=response.list
	        });
    	}
    	var aWatch=$scope.$watch('paginationConf.currentPage', SeaFun);
    }
    // $scope.$watch('paginationConf.currentPage + paginationConf.itemsPerPage'+$scope.suchchoice, $scope.Search);
    //导出
    $scope.extype=function(){
    	if($scope.keyValue==undefined){
    		var postSearch = {
	            now_page: $scope.paginationConf.currentPage,
	            page_rows: $scope.paginationConf.itemsPerPage,
	            suchchoice:'time',
	            type:'1'
	        }

			window.location.href=$rootScope.Url+'/priceInfo?startime='+$scope.timestart+'&endtime='+$scope.timend+'&now_page='+$scope.paginationConf.currentPage+'&page_rows='+$scope.paginationConf.itemsPerPage+'&excel=1';
    		return false;
    	}
    	var postSearch = {
            now_page: $scope.paginationConf.currentPage,
            page_rows: $scope.paginationConf.itemsPerPage,
            id:$scope.keyValue==undefined?'None':$scope.keyValue,
            timestart:$scope.timestart,
            timend:$scope.timend,
            type:$scope.suchchoice,
            extype:1,
       }

		$.ajax({
		    type: "POST",
		    url: 'suchactive',
		    data: postSearch,
		    success: function(response, status, request) {
		        var disp = request.getResponseHeader('Content-Disposition');
		        if (disp && disp.search('attachment') != -1) {
		            var form = $('<form method="POST" action="suchactive">');
		            $.each(postSearch, function(k, v) {
		                form.append($('<input type="hidden" name="' + k +'" value="' + v + '">'));
		            });
		            $('body').append(form);
		            form.submit();
		        }
		    }
		});


    }
	var file = document.getElementById('File');
	var formdata = new FormData();
	var Data;
	file.onchange=function(){
			console.log(this.files[0])
//			if(this.files[0].size/1024>5000){
//				showTips("请上传图片大小小于5M的图片");
//				return false;
//			}
		Data=this.files[0];
	$scope.Upload=function(){
		
		formdata.append("workImage",Data);
		$.ajax({
			type:"POST",
			url:"opload",
			async:false,
			timeout:'30000',
			data:formdata,
			dataType : "json",
	    	contentType: false,
	    	processData: false,
	    	success:function(response){
	    		console.log(response)
	    	}
		    })	
		}
		
	}
	
	
	
	
}])




//新增Rank-----------------------------------------

table.controller('RankId',['$routeParams','$scope','$http','$rootScope','BusinessService','PostService',function($routeParams,$scope,$http,$rootScope,BusinessService,PostService){
		$scope.countType=$routeParams.countType;
		$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
	//日历插件调用
	var d = new Date();
	//var str = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+(d.getDate()-1);
	$scope.timestart='2016-07-1';
	$scope.timend=d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();;
	var dateRange = new pickerDateRange('date_demo3', {
		//aRecent7Days : 'aRecent7DaysDemo3', //最近7天
		isTodayValid : false,
		startDate : '2016-07-1',
		endDate : $scope.timend,
		//needCompare : true,
		//isSingleDay : true,
		//shortOpr : true,
		defaultText : ' 至 ',
		inputTrigger : 'input_trigger_demo3',
		theme : 'ta',
		success : function(obj) {
			//$("#dCon_demo3").html('开始时间 : ' + obj.startDate + '<br/>结束时间 : ' + obj.endDate);
			$scope.timestart=obj.startDate;
			$scope.timend=obj.endDate;
			
		}
	});
	// 日历插件结束
	//配置分页基本参数
    $scope.paginationConf = {
        currentPage: 1,
        itemsPerPage: 5
    };
	//分页功能；
	$scope.suchchoice='time';
 	$scope.GetAllEmployee = function (num) {
 		if($scope.paginationConf.currentPage==0){
 			$scope.paginationConf.currentPage=1;
 		}
        var postData = {
        	startime:$scope.timestart,
	        endtime:$scope.timend,
            now_page: $scope.paginationConf.currentPage,
            page_rows: $scope.paginationConf.itemsPerPage,	
		    id:$routeParams.id,
//          suchchoice:num==undefined?'time':num,
         	type:0
        }
        BusinessService.list('fetchDay',postData).success(function (response) {
        	console.log(response)
            $scope.paginationConf.totalItems = response.total_count;
           	$scope.priceList=response.priceList
            
        });
    }
	
	//发送日奖品
	$scope.sendPrize=function(){
		$.ajax({
		    type: "POST",
		    url: 'sendPrize',
		    data: {id:$routeParams.id},
		    success: function(response) {
		        console.log(response);
		        if(response.result_code==0){
		        	alert('发放成功');
		        }
		        
		    }
		});
	}
	//发送周奖品
	$scope.accessToken=function(){
		$.ajax({
		    type: "POST",
		    url: 'accessToken',
		    data: {id:$routeParams.id},
		    success: function(response) {
		        console.log(response);
		        if(response.result_code==0){
		        	alert('发放成功');
		        }
		    }
		});
	}
	
    

    /***************************************************************
    	当页码和页面记录数发生变化时监控后台查询
    	如果把currentPage和itemsPerPage分开监控的话则会触发两次后台事件。 
    ***************************************************************/
    var unWatch=$scope.$watch('paginationConf.currentPage+paginationConf.itemsPerPage'+$scope.suchchoice, $scope.GetAllEmployee);
    
    //搜索
    $scope.extype=0;
    $scope.Search=function(){
    	unWatch();
    	function SeaFun() {
    		currentPage=$scope.paginationConf.currentPage<=0?'1':$scope.paginationConf.currentPage
	    	var postSearch = {
	            now_page: currentPage,
	            page_rows: $scope.paginationConf.itemsPerPage,
	            id:$scope.keyValue==''||$scope.keyValue==undefined?'None':$scope.keyValue,
	            startime:$scope.timestart,
	            endtime:$scope.timend,
	            type:$scope.suchchoice,
	            extype:0,
	        }
	    	PostService.list('fetchDay',postSearch).success(function (response) {
	    		console.log(response)
	    		if(response.total_count==0){
	    			aWatch();
	    		}
	            $scope.paginationConf.totalItems = response.total_count;
	            $scope.active = response.suchdata;
	        });
    	}
    	var aWatch=$scope.$watch('paginationConf.currentPage', SeaFun);
    }
    // $scope.$watch('paginationConf.currentPage + paginationConf.itemsPerPage'+$scope.suchchoice, $scope.Search);
    //导出
    $scope.extype=function(){
    	//if($scope.keyValue==undefined){
    		var postSearch = {
	            now_page: $scope.paginationConf.currentPage,
	            page_rows: $scope.paginationConf.itemsPerPage,
	            //suchchoice:'time',
	            type:'1'
	        }

			window.location.href=$rootScope.Url+'/fetchDay?type=1&id='+$routeParams.id+'&now_page='+$scope.paginationConf.currentPage+'&page_rows='+$scope.paginationConf.itemsPerPage;
    		return false;
    	//}
//  	var postSearch = {
//          now_page: $scope.paginationConf.currentPage,
//          page_rows: $scope.paginationConf.itemsPerPage,
//          id:$routeParams.id,
//          startime:$scope.timestart,
//          timend:$scope.timend,
//          type:1,
//     }

//		$.ajax({
//		    type: "POST",
//		    url: 'fetchCount',
//		    data: postSearch,
//		    success: function(response, status, request) {
//		        var disp = request.getResponseHeader('Content-Disposition');
//		        if (disp && disp.search('attachment') != -1) {
//		            var form = $('<form method="POST" action="fetchCount">');
//		            $.each(postSearch, function(k, v) {
//		                form.append($('<input type="hidden" name="' + k +'" value="' + v + '">'));
//		            });
//		            $('body').append(form);
//		            form.submit();
//		        }
//		    }
//		});


    }

	
}])


table.controller('Rank',['$scope','$http','$rootScope','BusinessService','PostService',function($scope,$http,$rootScope,BusinessService,PostService){
	$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
	//日历插件调用
	var d = new Date();
	//var str = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+(d.getDate()-1);
	$scope.timestart='2016-07-1';
	$scope.timend=d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();
	var dateRange = new pickerDateRange('date_demo3', {
		//aRecent7Days : 'aRecent7DaysDemo3', //最近7天
		isTodayValid : false,
		startDate : '2016-07-1',
		endDate : $scope.timend,
		//needCompare : true,
		//isSingleDay : true,
		//shortOpr : true,
		defaultText : ' 至 ',
		inputTrigger : 'input_trigger_demo3',
		theme : 'ta',
		success : function(obj) {
			//$("#dCon_demo3").html('开始时间 : ' + obj.startDate + '<br/>结束时间 : ' + obj.endDate);
			$scope.timestart=obj.startDate;
			$scope.timend=obj.endDate;
			
		}
	});
	// 日历插件结束
	//配置分页基本参数
    $scope.paginationConf = {
        currentPage: 1,
        itemsPerPage: 5
    };
	//分页功能；
	$scope.suchchoice='time';
 	$scope.GetAllEmployee = function (num) {
        var postData = {
        	startime:$scope.timestart,
	        endtime:$scope.timend,
            now_page: $scope.paginationConf.currentPage,
            page_rows: $scope.paginationConf.itemsPerPage,
//          suchchoice:num==undefined?'time':num,
//          type:'0'
        }
        BusinessService.list('fetchmumber').success(function (response) {
        	console.log(response)
            $scope.paginationConf.totalItems = response.total_count;
            $scope.priceList = response.countList;
            
        });
    }
	
	$.ajax({
		    type: "get",
		    url: 'makeWeek',
		    success: function(response) {
		        console.log(response);
		    }
		});
		$.ajax({
		    type: "get",
		    url: 'dayCount',
		    success: function(response) {
		        console.log(response);
		    }
		});
	
    

    /***************************************************************
    	当页码和页面记录数发生变化时监控后台查询
    	如果把currentPage和itemsPerPage分开监控的话则会触发两次后台事件。 
    ***************************************************************/
    var unWatch=$scope.$watch('paginationConf.currentPage+paginationConf.itemsPerPage'+$scope.suchchoice, $scope.GetAllEmployee);
    
    //搜索
    $scope.extype=0;
    $scope.Search=function(){
    	unWatch();
    	function SeaFun() {
    		currentPage=$scope.paginationConf.currentPage<=0?'1':$scope.paginationConf.currentPage
	    	var postSearch = {
	            now_page: currentPage,
	            page_rows: $scope.paginationConf.itemsPerPage,
	            id:$scope.keyValue==''||$scope.keyValue==undefined?'None':$scope.keyValue,
	            startime:$scope.timestart,
	            endtime:$scope.timend,
	            type:$scope.suchchoice,
	            extype:0,
	        }
	    	PostService.list('fetchDay',postSearch).success(function (response) {
	    		console.log(response)
	    		if(response.total_count==0){
	    			aWatch();
	    		}
	            $scope.paginationConf.totalItems = response.total_count;
	            $scope.active = response.suchdata;
	        });
    	}
    	var aWatch=$scope.$watch('paginationConf.currentPage', SeaFun);
    }
    // $scope.$watch('paginationConf.currentPage + paginationConf.itemsPerPage'+$scope.suchchoice, $scope.Search);
    //导出
    $scope.extype=function(){
    	if($scope.keyValue==undefined){
    		var postSearch = {
	            now_page: $scope.paginationConf.currentPage,
	            page_rows: $scope.paginationConf.itemsPerPage,
	            suchchoice:'time',
	            type:'1'
	        }

			window.location.href=$rootScope.Url+'/fetchDay?now_page='+$scope.paginationConf.currentPage+'&page_rows='+$scope.paginationConf.itemsPerPage;
    		return false;
    	}
    	var postSearch = {
            now_page: $scope.paginationConf.currentPage,
            page_rows: $scope.paginationConf.itemsPerPage,
            id:$scope.keyValue==undefined?'None':$scope.keyValue,
            timestart:$scope.timestart,
            timend:$scope.timend,
            type:$scope.suchchoice,
            extype:1,
       }

		$.ajax({
		    type: "POST",
		    url: 'suchactive',
		    data: postSearch,
		    success: function(response, status, request) {
		        var disp = request.getResponseHeader('Content-Disposition');
		        if (disp && disp.search('attachment') != -1) {
		            var form = $('<form method="POST" action="suchactive">');
		            $.each(postSearch, function(k, v) {
		                form.append($('<input type="hidden" name="' + k +'" value="' + v + '">'));
		            });
		            $('body').append(form);
		            form.submit();
		        }
		    }
		});


    }
}]);


//Rank-----------------------------------

table.run(['$rootScope','$window','$http',function($rootScope,$window,$http){
	//获取pv/uv
	$rootScope.Url='/ticai/back';
//上线需放开	
	//$rootScope.Url='http://192.168.100.250:8000/ticai/back';
	if(!sessionStorage.cookie){
		$window.location.href=$rootScope.Url+'/viste.html';
	};
	//获取uv,pv；    
    $http.get('puv').success(function(data){
		$rootScope.pv=data.pv;
		$rootScope.uv=data.uv;
	})
	
}])
table.controller('Active',['$scope','$http','$rootScope','BusinessService','PostService',function($scope,$http,$rootScope,BusinessService,PostService){
	$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
	//日历插件调用
	var d = new Date();
	var unWatch,unWatchs;
	//var str = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+(d.getDate()-1);
	$scope.timestart='2016-07-1';
	$scope.timend=d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();;
	var dateRange = new pickerDateRange('date_demo3', {
		//aRecent7Days : 'aRecent7DaysDemo3', //最近7天
		isTodayValid : false,
		startDate : '2016-07-1',
		endDate : $scope.timend,
		//needCompare : true,
		//isSingleDay : true,
		//shortOpr : true,
		defaultText : ' 至 ',
		inputTrigger : 'input_trigger_demo3',
		theme : 'ta',
		success : function(obj) {
			//$("#dCon_demo3").html('开始时间 : ' + obj.startDate + '<br/>结束时间 : ' + obj.endDate);
			$scope.timestart=obj.startDate;
			$scope.timend=obj.endDate;
			
		}
	});
	// 日历插件结束
	
	//分页功能；
	$scope.suchchoice='time';
	$scope.Time=0;
	$scope.num=0;
 	$scope.GetAllEmployee = function (num) {
 		if(num=='time'){
 			$scope.num='time'
 		}else if(num=='None'){
 			$scope.num='None'
 		}
 		if($scope.keyValue&&num=='time'){
 			$scope.Time='time';
 		}else if($scope.keyValue&&num=='None'){
 			$scope.Time=0
 		}
 		if($scope.paginationConf.currentPage==0){
        	$scope.paginationConf.currentPage=1;
        }
        var postData = {
            now_page: $scope.paginationConf.currentPage,
            page_rows: $scope.paginationConf.itemsPerPage,
            suchchoice:$scope.num,
            timestart:$scope.timestart,
            timend:$scope.timend,
            type:$scope.Time,
            extype:'',
            id:$scope.keyValue
        }
        
        if($scope.keyValue){
        	PostService.list('suchactive',postData).success(function (response) {
	            $scope.paginationConf.totalItems = response.total_count;
	            $scope.active = response.suchdata;
	        });
        }else{
        	BusinessService.list('activedata',postData).success(function (response) {
	            $scope.paginationConf.totalItems = response.total_count;
	            $scope.active = response.acivedata;
	        });
        }
        
    }
//	$scope.searchEmployee = function (num) {
//		unWatch();
// 		if(num=='time'){
// 			$scope.Time='time'
// 		}else if(num=='None'|| num==''||num==undefined){
// 			$scope.Time='none'
// 		}
//      var postData = {
//          now_page: $scope.paginationConf.currentPage,
//          page_rows: $scope.paginationConf.itemsPerPage,
//          suchchoice:$scope.Time,
//          timestart:$scope.timestart,
//          timend:$scope.timend,
//          type:$scope.Time,
//          extype:''
//      }
//      PostService.list('suchactive',postData).success(function (response) {
//      	if(response.total_count==0){
//      		response.total_count=1;
//      	}
//          $scope.paginationConf.totalItems = response.total_count;
//          $scope.active = response.suchdata;
//      });
//  }
    //配置分页基本参数
    $scope.paginationConf = {
        currentPage: 1,
        itemsPerPage: 5
    };

    /***************************************************************
    	当页码和页面记录数发生变化时监控后台查询
    	如果把currentPage和itemsPerPage分开监控的话则会触发两次后台事件。 
    ***************************************************************/
    unWatch=$scope.$watch('paginationConf.currentPage+paginationConf.itemsPerPage', $scope.GetAllEmployee);
    unWatch_1=$scope.$watch('paginationConf.currentPage+paginationConf.itemsPerPage', $scope.searchEmployee);
    //搜索
    $scope.extype=0;
    $scope.Search=function(){
    	unWatch();
    	function SeaFun() {
    		currentPage=$scope.paginationConf.currentPage<=0?'1':$scope.paginationConf.currentPage
	    	var postSearch = {
	            now_page: currentPage,
	            page_rows: $scope.paginationConf.itemsPerPage,
	            id:$scope.keyValue==''||$scope.keyValue==undefined?'None':$scope.keyValue,
	            timestart:$scope.timestart,
	            suchchoice:$scope.Time,
	            timend:$scope.timend,
	            type:$scope.Time,
	            extype:0,
	        }
	    	PostService.list('suchactive',postSearch).success(function (response) {
	    		if(response.total_count==0){
	    			aWatch();
	    		}
	            $scope.paginationConf.totalItems = response.total_count;
	            $scope.active = response.suchdata;
	        });
    	}
    	var aWatch=$scope.$watch('paginationConf.currentPage', SeaFun);
    }
    // $scope.$watch('paginationConf.currentPage + paginationConf.itemsPerPage'+$scope.suchchoice, $scope.Search);
    //导出
    $scope.extype=function(){
    	if($scope.keyValue==undefined){
    		var postSearch = {
	            now_page: $scope.paginationConf.currentPage,
	            page_rows: $scope.paginationConf.itemsPerPage,
	            suchchoice:'time',
	            type:'1',
	            timestart:$scope.timestart,
	            timend:$scope.timend,
	        }

			window.location.href=$rootScope.Url+'/activedata?timestart='+$scope.timestart+'&timend='+$scope.timend+'&now_page='+$scope.paginationConf.currentPage+'&page_rows='+$scope.paginationConf.itemsPerPage+'&suchchoice=time&type=1';
    		return false;
    	}
    	var postSearch = {
            now_page: $scope.paginationConf.currentPage,
            page_rows: $scope.paginationConf.itemsPerPage,
            id:$scope.keyValue==undefined?'None':$scope.keyValue,
            timestart:$scope.timestart,
            timend:$scope.timend,
            type:$scope.suchchoice,
            extype:1,
       }

		$.ajax({
		    type: "POST",
		    url: 'suchactive',
		    data: postSearch,
		    success: function(response, status, request) {
		        var disp = request.getResponseHeader('Content-Disposition');
		        if (disp && disp.search('attachment') != -1) {
		            var form = $('<form method="POST" action="suchactive">');
		            $.each(postSearch, function(k, v) {
		                form.append($('<input type="hidden" name="' + k +'" value="' + v + '">'));
		            });
		            $('body').append(form);
		            form.submit();
		        }
		    }
		});


    }
    // 修改步数
    
    $('body').on('click','.but',function(){
    	var This=$(this);
    	var dataCid=$(this).attr('data-cid');
    	var dataNum=$(this).attr('data-num');
    	if($('#'+dataNum).attr('disabled')=='disabled'){
    		This.addClass('color');
    		$('#'+dataNum).attr('disabled',false);
    		return false;
    	}else{
    		var Val=$('#'+dataNum).val();
//  		if(Val<0){
//  			return false;
//  		}
    		var ChangeList={
    			Cid:dataCid,
    			change:Val
    		}
    		$http({
    			method:'POST',
    			url:'change',
    			data:$.param(ChangeList)
    		}).success(function(){
    			This.removeClass('color');
    			$('#'+dataNum).attr('disabled',true);
    		})
    		
    	}
    })
    
}]);


//线下报名

table.controller('Offline',['$rootScope','$scope','$http','BusinessService','PostService',function($rootScope,$scope,$http,BusinessService,PostService){
	$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
	//日历插件调用
	var d = new Date();
	//var str = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+(d.getDate()-1);
	$scope.timestart='2016-07-1';
	$scope.timend=d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();;
	var dateRange = new pickerDateRange('date_demo3', {
		//aRecent7Days : 'aRecent7DaysDemo3', //最近7天
		isTodayValid : false,
		startDate : '2016-07-1',
		endDate : $scope.timend,
		//needCompare : true,
		//isSingleDay : true,
		//shortOpr : true,
		defaultText : ' 至 ',
		inputTrigger : 'input_trigger_demo3',
		theme : 'ta',
		success : function(obj) {
			//$("#dCon_demo3").html('开始时间 : ' + obj.startDate + '<br/>结束时间 : ' + obj.endDate);
			$scope.timestart=obj.startDate;
			$scope.timend=obj.endDate;
			
		}
	});
	// 日历插件结束
	
	var GetAllEmployee = function () {
        var postData = {
            now_page: $scope.paginationConf.currentPage,
            page_rows: $scope.paginationConf.itemsPerPage,
            timestart:$scope.timestart,
	        timend:$scope.timend,
            type:'0'
        }
        if($scope.paginationConf.currentPage==0){
        	$scope.paginationConf.currentPage=1;
        }
        BusinessService.list('signup',postData).success(function (response) {
            $scope.paginationConf.totalItems = response.total_count;
            $scope.active = response.signup;
        });
    }

    //配置分页基本参数
    $scope.paginationConf = {
        currentPage: 1,
        itemsPerPage: 5
    };
    /***************************************************************
    	当页码和页面记录数发生变化时监控后台查询
    	如果把currentPage和itemsPerPage分开监控的话则会触发两次后台事件。 
    ***************************************************************/
    var unWatch=$scope.$watch('paginationConf.currentPage+paginationConf.itemsPerPage', GetAllEmployee);
    //搜索
    $scope.Search=function(){
    	unWatch();
    	function SeaFun() {
    		currentPage=$scope.paginationConf.currentPage<=0?'1':$scope.paginationConf.currentPage
	    	var postSearch = {
	            now_page: currentPage,
	            page_rows: $scope.paginationConf.itemsPerPage,
	            id:$scope.keyValue==''||$scope.keyValue==undefined?'None':$scope.keyValue,
	            timestart:$scope.timestart,
	            timend:$scope.timend,
	            type:0
	        }
	    	PostService.list('suchsign',postSearch).success(function (response) {
	    		if(response.total_count==0){
	    			aWatch();
	    		}
	            $scope.paginationConf.totalItems = response.total_count;
	            $scope.active = response.signup;
	        });
    	}
    	var aWatch=$scope.$watch('paginationConf.currentPage', SeaFun);
    }
   //导出
    $scope.extype=function(){
    	if($scope.keyValue==undefined){
	    	var postSearch = {
		            now_page: $scope.paginationConf.currentPage,
		            page_rows: $scope.paginationConf.itemsPerPage,
		            suchchoice:'time',
		            type:'1'
		        }
			window.location.href=$rootScope.Url+'/signup?now_page='+$scope.paginationConf.currentPage+'&page_rows='+$scope.paginationConf.itemsPerPage+'&suchchoice=time&type=1';
    		return false;
    	}
    	var postSearch = {
            now_page: $scope.paginationConf.currentPage,
            page_rows: $scope.paginationConf.itemsPerPage,
            id:$scope.keyValue==undefined?'None':$scope.keyValue,
            timestart:$scope.timestart,
            timend:$scope.timend,
            type:1,
        }
    	//PostService.list('suchsign',postSearch)
    	$.ajax({
		    type: "POST",
		    url: 'suchsign',
		    data: postSearch,
		    success: function(response, status, request) {
		        var disp = request.getResponseHeader('Content-Disposition');
		        if (disp && disp.search('attachment') != -1) {
		            var form = $('<form method="POST" action="suchsign">');
		            $.each(postSearch, function(k, v) {
		                form.append($('<input type="hidden" name="' + k +'" value="' + v + '">'));
		            });
		            $('body').append(form);
		            form.submit();
		        }
		    }
		});
    }
    
    
    
}]);
//奖品数据
table.controller('Award',['$rootScope','$scope','$http','BusinessService','PostService',function($rootScope,$scope,$http,BusinessService,PostService){
	$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
	$scope.week=1;
	 //配置分页基本参数
    $scope.paginationConf = {
        currentPage: 1,
        itemsPerPage: 5
    };
	//日历插件调用
	var d = new Date();
	//var str = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+(d.getDate()-1);
	$scope.timestart='2016-07-1';
	$scope.timend=d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();;
	var dateRange = new pickerDateRange('date_demo3', {
		//aRecent7Days : 'aRecent7DaysDemo3', //最近7天
		isTodayValid : false,
		startDate : '2016-07-1',
		endDate : $scope.timend,
		//needCompare : true,
		//isSingleDay : true,
		//shortOpr : true,
		defaultText : ' 至 ',
		inputTrigger : 'input_trigger_demo3',
		theme : 'ta',
		success : function(obj) {
			//$("#dCon_demo3").html('开始时间 : ' + obj.startDate + '<br/>结束时间 : ' + obj.endDate);
			$scope.timestart=obj.startDate;
			$scope.timend=obj.endDate;
			
		}
	});
	// 日历插件结束
	var GetAllEmployee = function () {
        var postData = {
            now_page: $scope.paginationConf.currentPage,
            page_rows: $scope.paginationConf.itemsPerPage,
            type:'0',
            week:$scope.week,
        }
        BusinessService.list('swprices',postData).success(function (response) {
            $scope.paginationConf.totalItems = response.total_page;
            $scope.active = response.swdata;
        });
    }
	$scope.showList=function(num){
		$scope.week=num
	}
    /***************************************************************
    	当页码和页面记录数发生变化时监控后台查询
    	如果把currentPage和itemsPerPage分开监控的话则会触发两次后台事件。 
    ***************************************************************/
    var unWatch=$scope.$watch('paginationConf.currentPage+week', GetAllEmployee);
    //搜索
    $scope.Search=function(){
    	unWatch();
    	function SeaFun() {
    		currentPage=$scope.paginationConf.currentPage<=0?'1':$scope.paginationConf.currentPage
	    	var postSearch = {
	            now_page: currentPage,
	            page_rows: $scope.paginationConf.itemsPerPage,
	            id:$scope.keyValue==''||$scope.keyValue==undefined?'None':$scope.keyValue,
	            //timestart:$scope.timestart,
	            //timend:$scope.timend,
	            type:0,
	            week:$scope.week,
	        }
	    	BusinessService.list('swprices',postSearch).success(function (response) {
	    		if(response.total_page==0){
	    			aWatch();
	    		}
	            $scope.paginationConf.totalItems = response.total_page;
	            $scope.active = response.swdata;
	        });
    	}
    	var aWatch=$scope.$watch('paginationConf.currentPage', SeaFun);
    }
    //导出
    $scope.extype=function(){
    	if($scope.keyValue==undefined){
	    	var postSearch = {
		            now_page: $scope.paginationConf.currentPage,
		            page_rows: $scope.paginationConf.itemsPerPage,
		            suchchoice:'time',
		            type:1,
		            week:$scope.week,
		        }
			window.location.href=$rootScope.Url+'/swprices?week='+$scope.week+'&now_page='+$scope.paginationConf.currentPage+'&page_rows='+$scope.paginationConf.itemsPerPage+'&type=1';
    		return false;
    	}
    	
//  	var postSearch = {
//          now_page: $scope.paginationConf.currentPage,
//          page_rows: $scope.paginationConf.itemsPerPage,
//          id:$scope.keyValue==undefined?'None':$scope.keyValue,
//          timestart:$scope.timestart,
//          timend:$scope.timend,
//          //suchchoice:'time',
//          type:1,
//          week:$scope.week,
//      }
    	//PostService.list('suchsw',postSearch);
//  	$.ajax({
//		    type: "POST",
//		    url: 'suchsw',
//		    data: postSearch,
//		    success: function(response, status, request) {
//		        var disp = request.getResponseHeader('Content-Disposition');
//		        if (disp && disp.search('attachment') != -1) {
//		            var form = $('<form method="POST" action="suchsw">');
//		            $.each(postSearch, function(k, v) {
//		                form.append($('<input type="hidden" name="' + k +'" value="' + v + '">'));
//		            });
//		            $('body').append(form);
//		            form.submit();
//		        }
//		    }
//		});
    }
    
	
}]);
//用户数据
table.controller('User',['$rootScope','$scope','$http','BusinessService','PostService',function($rootScope,$scope,$http,BusinessService,PostService){
	$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
	//日历插件调用
	var d = new Date();
	//var str = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+(d.getDate()-1);
	$scope.timestart='2016-07-1';
	$scope.timend=d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();;
	var dateRange = new pickerDateRange('date_demo3', {
		//aRecent7Days : 'aRecent7DaysDemo3', //最近7天
		isTodayValid : false,
		startDate : '2016-07-1',
		endDate : $scope.timend,
		//needCompare : true,
		//isSingleDay : true,
		//shortOpr : true,
		defaultText : ' 至 ',
		inputTrigger : 'input_trigger_demo3',
		theme : 'ta',
		success : function(obj) {
			//$("#dCon_demo3").html('开始时间 : ' + obj.startDate + '<br/>结束时间 : ' + obj.endDate);
			$scope.timestart=obj.startDate;
			$scope.timend=obj.endDate;
			
		}
	});
	// 日历插件结束
	$scope.Time='none';
	
	$scope.GetAllEmployee = function (num) {
		if(num=='time'){
	 		$scope.Time='time'
		}else if(num=='None'){
			$scope.Time='none'
		}
        var postData = {
            now_page: $scope.paginationConf.currentPage,
            page_rows: $scope.paginationConf.itemsPerPage,
            suchchoice:$scope.Time,
            type:'',
            timestart:$scope.timestart,
            timend:$scope.timend
        }
        BusinessService.list('userdata',postData).success(function (response) {
            $scope.paginationConf.totalItems = response.total_page;
            $scope.active = response.userdata;
        });
    }

    //配置分页基本参数
    $scope.paginationConf = {
        currentPage: 1,
        itemsPerPage: 5
    };

    /***************************************************************
    	当页码和页面记录数发生变化时监控后台查询
    	如果把currentPage和itemsPerPage分开监控的话则会触发两次后台事件。 
    ***************************************************************/
    var unWatch=$scope.$watch('paginationConf.currentPage+paginationConf.itemsPerPage', $scope.GetAllEmployee);
    //搜索
    $scope.Search=function(){
    	unWatch();
    	function SeaFun() {
    		currentPage=$scope.paginationConf.currentPage<=0?'1':$scope.paginationConf.currentPage
	    	var postSearch = {
	            now_page: currentPage,
	            page_rows: $scope.paginationConf.itemsPerPage,
	            id:$scope.keyValue==''||$scope.keyValue==undefined?'None':$scope.keyValue,
	            suchchoice:'time',
	            type:0,
	            timestart:$scope.timestart,
            	timend:$scope.timend
	        }
	    	
	    	if($scope.keyValue==''||$scope.keyValue==undefined){
	    		BusinessService.list('userdata',postSearch).success(function (response) {
		    		if(response.total_count==0){
		    			aWatch();
		    		}
		            $scope.paginationConf.totalItems = response.total_page;
		            $scope.active = response.userdata;
		        });
	    	}else{
		    	PostService.list('suchuser',postSearch).success(function (response) {
		    		if(response.total_count==0){
		    			aWatch();
		    		}
		            $scope.paginationConf.totalItems = response.total_page;
		            $scope.active = response.userdata;
		        });
	       }
    	}
    	var aWatch=$scope.$watch('paginationConf.currentPage', SeaFun);
    }
    
    //导出
    $scope.extype=function(){
    	console.log(1111)
    	if($scope.keyValue==undefined){
	    	var postSearch = {
		            now_page: $scope.paginationConf.currentPage,
		            page_rows: $scope.paginationConf.itemsPerPage,
		            suchchoice:'time',
		            type:'1'
		        }
			window.location.href=$rootScope.Url+'/userdata?now_page='+$scope.paginationConf.currentPage+'&page_rows='+$scope.paginationConf.itemsPerPage+'&suchchoice='+$scope.Time+'&type=1';
    		return false;
    	}
    	
    	var postSearch = {
            now_page: $scope.paginationConf.currentPage,
            page_rows: $scope.paginationConf.itemsPerPage,
            id:$scope.keyValue==undefined?'None':$scope.keyValue,
            timestart:$scope.timestart,
            timend:$scope.timend,
            suchchoice:$scope.Time,
            type:1,
        }
    	//PostService.list('suchsw',postSearch);
    	$.ajax({
		    type: "POST",
		    url: 'userdata',
		    data: postSearch,
		    success: function(response, status, request) {
		        var disp = request.getResponseHeader('Content-Disposition');
		        if (disp && disp.search('attachment') != -1) {
		            var form = $('<form method="POST" action="suchsw">');
		            $.each(postSearch, function(k, v) {
		                form.append($('<input type="hidden" name="' + k +'" value="' + v + '">'));
		            });
		            $('body').append(form);
		            form.submit();
		        }
		    }
		});
    }
    
    
    
    
    
    
    
	
}])

//查询单个用户信息
table.controller('UserFind',['$scope','$routeParams','$http','BusinessService','PostService',function($scope,$routeParams,$http,BusinessService,PostService){
	$scope.userId=$routeParams.id;
	$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
	//日历插件调用
	var d = new Date();
	//var str = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+(d.getDate()-1);
	$scope.timestart='2016-07-1';
	$scope.timend=d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();;
	var dateRange = new pickerDateRange('date_demo3', {
		//aRecent7Days : 'aRecent7DaysDemo3', //最近7天
		isTodayValid : false,
		startDate : '2016-07-1',
		endDate : $scope.timend,
		//needCompare : true,
		//isSingleDay : true,
		//shortOpr : true,
		defaultText : ' 至 ',
		inputTrigger : 'input_trigger_demo3',
		theme : 'ta',
		success : function(obj) {
			//$("#dCon_demo3").html('开始时间 : ' + obj.startDate + '<br/>结束时间 : ' + obj.endDate);
			$scope.timestart=obj.startDate;
			$scope.timend=obj.endDate;
			
		}
	});
	// 日历插件结束
	//分页功能；
	$scope.suchchoice='time';
 	$scope.GetAllEmployee = function (num) {
        var postSearch = {
	            now_page: $scope.paginationConf.currentPage,
	            page_rows: $scope.paginationConf.itemsPerPage,
	            id:$scope.userId,
	            timestart:$scope.timestart,
	            timend:$scope.timend,
	            type:num==undefined?'time':num,
	            extype:0,
	        }
	    	PostService.list('suchactive',postSearch).success(function (response) {
	            $scope.paginationConf.totalItems = response.total_count;
	            $scope.active = response.suchdata;
	        });
    }

    //配置分页基本参数
    $scope.paginationConf = {
        currentPage: 1,
        itemsPerPage: 5
    };

    /***************************************************************
    	当页码和页面记录数发生变化时监控后台查询
    	如果把currentPage和itemsPerPage分开监控的话则会触发两次后台事件。 
    ***************************************************************/
    var unWatch=$scope.$watch('paginationConf.currentPage+paginationConf.itemsPerPage'+$scope.suchchoice, $scope.GetAllEmployee);
    
    //搜索
    $scope.extype=0;
    $scope.Search=function(){
    	unWatch();
    	function SeaFun() {
    		currentPage=$scope.paginationConf.currentPage<=0?'1':$scope.paginationConf.currentPage
	    	var postSearch = {
	            now_page: currentPage,
	            page_rows: $scope.paginationConf.itemsPerPage,
	            id:$scope.keyValue==''||$scope.keyValue==undefined?'None':$scope.keyValue,
	            timestart:$scope.timestart,
	            timend:$scope.timend,
	            type:$scope.suchchoice,
	            extype:0,
	        }
	    	PostService.list('suchactive',postSearch).success(function (response) {
	    		if(response.total_count==0){
	    			aWatch();
	    		}
	            $scope.paginationConf.totalItems = response.total_count;
	            $scope.active = response.suchdata;
	        });
    	}
    	var aWatch=$scope.$watch('paginationConf.currentPage', SeaFun);
    }
    // $scope.$watch('paginationConf.currentPage + paginationConf.itemsPerPage'+$scope.suchchoice, $scope.Search);
    //导出
    $scope.extype=function(){
    	var postSearch = {
            now_page: $scope.paginationConf.currentPage,
            page_rows: $scope.paginationConf.itemsPerPage,
            id:$scope.userId,
            timestart:$scope.timestart,
            timend:$scope.timend,
            type:$scope.suchchoice,
            extype:1,
        }
    	//PostService.list('suchactive',postSearch);
    	$.ajax({
		    type: "POST",
		    url: 'suchactive',
		    data: postSearch,
		    success: function(response, status, request) {
		        var disp = request.getResponseHeader('Content-Disposition');
		        if (disp && disp.search('attachment') != -1) {
		            var form = $('<form method="POST" action="suchactive">');
		            $.each(postSearch, function(k, v) {
		                form.append($('<input type="hidden" name="' + k +'" value="' + v + '">'));
		            });
		            $('body').append(form);
		            form.submit();
		        }
		    }
		});
    	
    }
    // 修改步数
     $('body').on('click','.but',function(){
    	var This=$(this);
    	var dataCid=$(this).attr('data-cid');
    	var dataNum=$(this).attr('data-num');
    	if($('#'+dataNum).attr('disabled')=='disabled'){
    		This.addClass('color');
    		$('#'+dataNum).attr('disabled',false);
    		return false;
    	}else{
    		var Val=Number($('#'+dataNum).val());
    		if(Val<=0){
    			return false;
    		}
    		var ChangeList={
    			Cid:dataCid,
    			change:Val
    		}
    		$http({
    			method:'POST',
    			url:'change',
    			data:$.param(ChangeList)
    		}).success(function(){
    			This.removeClass('color');
    			$('#'+dataNum).attr('disabled',true);
    		})
    		
    	}
    })
}]);

//奖品设置
table.controller('Draw',['$scope','$http',function($scope,$http){
	$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
	$scope.fu=function(){
		$http({
			method:'get',
			url:'loadFile'
		}).success(function(response){
			$scope.data=response.data;
		});
	}
	$scope.fu();
	
	$scope.shengc=function(ID){
		$http({
			method:'get',
			url:'startAdd?id='+ID,
		}).success(function(response){
			alert('成功')
		});
	}
	
	$scope.add=function(){
		$scope.addpro=true;
	}
	
	$scope.addData=function(){
		var ChangeList={
    			maxmon:$scope.add_maxmon,
    			prichance:$scope.add_prichance,
    			FiChance:$scope.add_FiChance
    		}
    		$http({
    			method:'POST',
    			url:'lotteryset',
    			data:$.param(ChangeList)
    		}).success(function(data){
    			if(data.result_code==1){
    				alert('添加失败，错误提示'+data.result_msg);
    				return false;
    			}
    			$scope.addpro=false;
    			$scope.fu();
    		})
	}
	
	$('body').off('click');
	$('body').on('click','.buts',function(){
    	var This=$(this);
    	var dataNum=$(this).attr('data-num');
    	if($('#'+dataNum).attr('data-dis')==undefined||$('#'+dataNum).attr('data-dis')==''){
    		This.addClass('color');
    		This.val('确认');
    		$('#'+dataNum).attr('data-dis','ok');
    		$('#'+dataNum).find('input[type=number]').attr('disabled',false);
    	}else{
    		$('#'+dataNum).attr('data-dis','');
    		var ChangeList={
    			maxmon:$scope.maxmon,
    			prichance:$scope.prichance,
    			FiChance:$scope.FiChance
    		}
    		$http({
    			method:'POST',
    			url:'lotteryset',
    			data:$.param(ChangeList)
    		}).success(function(){
    			This.removeClass('color');
    			This.val('修改')
    			$('#'+dataNum).find('input[type=number]').attr('disabled',true);
    		})
    		
    	}
    	return false;
    })
	
	
}])
//奖池设置
table.controller('Progressive',['$scope','$http',function($scope,$http){
	$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
	
	//日历插件调用
	var d = new Date();
	//var str = d.getFullYear()+"-"+(d.getMonth()+1)+"-"+(d.getDate()-1);
	$scope.timestart='2016-07-1';
	$scope.timend=d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();;
	var dateRange = new pickerDateRange('date_demo3', {
		//aRecent7Days : 'aRecent7DaysDemo3', //最近7天
		isTodayValid : false,
		startDate : '2016-07-1',
		endDate : $scope.timend,
		//needCompare : true,
		//isSingleDay : true,
		//shortOpr : true,
		defaultText : ' 至 ',
		inputTrigger : 'input_trigger_demo3',
		theme : 'ta',
		success : function(obj) {
			//$("#dCon_demo3").html('开始时间 : ' + obj.startDate + '<br/>结束时间 : ' + obj.endDate);
			$scope.timestart=obj.startDate;
			$scope.timend=obj.endDate;
			
		}
	});
	
	
	
	
	$scope.fu=function(){
		
		$http({
			method:'get',
			url:'dayPuv',
			params:{
				endtime:$scope.timend,
				startime:$scope.timestart
			}
		}).success(function(response){
			$scope.data=response
		})
	}
	
	$scope.See=function(){
		$scope.fu();
	}
	$scope.fu();
	//$scope.$watch('timend+timestart', $scope.fu());
	$scope.add=function(){
		$scope.addpro=true;
	}
	
	$scope.addData=function(){
		if($scope.add_pricetype==0){
			var pmoney=$('input[name=pricemoney]').val().trim();
		}else{
			var pmoney=0;
		}
		return false;
		var ChangeList={
    			pricename:$scope.add_pricename,
    			pricetype:$scope.add_pricetype,
    			pricecount:$scope.add_pricecount,
    			pricemon:pmoney
    		}
    		$http({
    			method:'POST',
    			url:'priceset',
    			data:$.param(ChangeList)
    		}).success(function(data){
    			if(data.result_code==1){
    				alert('添加失败，错误提示'+data.result_msg);
    				return false;
    			}
    			$scope.addpro=false;
    			$scope.fu();
    		})
	}
	
}])

table.factory('PostService', ['$http', function ($http) {
    var list = function (Path,postData) {
        return $http({
        	method:'post',
        	url:Path,
        	data:$.param(postData),
        	dataType:'json'
        });
    }

    return {
        list: function (Path,postData) {
            return list(Path,postData);
        }
    }
}]);

    //get业务类
table.factory('BusinessService', ['$http', function ($http) {
    var list = function (Path,postData) {
        return $http({
        	method:'get',
        	url:Path,
        	params:postData,
        });
    }

    return {
        list: function (Path,postData) {
            return list(Path,postData);
        }
    }
}]);


//手动加载多个ng-app
angular.element(document).ready(
   function (){
    angular.bootstrap(document.getElementById("right"), ["myTable"]);
   }
 );