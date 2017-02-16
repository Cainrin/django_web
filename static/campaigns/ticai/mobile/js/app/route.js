//右侧路由控制
var table=angular.module('myTable',['ngRoute','ngSanitize']);
table.config(function($routeProvider){
	$routeProvider.when('/',{
		templateUrl:'/static/campaigns/ticai/mobile/view/index.html',
		controller:'Index'
	})
	.when('/successIndex',{
		templateUrl:'/static/campaigns/ticai/mobile/view/indexSuccess.html',
		controller:'successIndex'
	}).when('/list',{
		templateUrl:'/static/campaigns/ticai/mobile/view/list.html',
		controller:'List'
	})
	.when('/prize',{
		templateUrl:'/static/campaigns/ticai/mobile/view/prize.html',
		controller:'Prize'
	})
	.when('/signUp',{
		templateUrl:'/static/campaigns/ticai/mobile/view/signUp.html',
		controller:'SignUp'
	})
	.when('/explain',{
		templateUrl:'/static/campaigns/ticai/mobile/view/explain.html',
		//controller:'Explain'
	})
	.otherwise({
		redirectTo:'/'
	})
});
//处理时间换行
table.filter('TimeFile',function(){
	return function(val){
		var val=val.split(' ').join('<br/>');
		console.log(val);
		return val;
	}
})
//处理6位字符串补全
table.filter('complete',function(){
	return function(val){
		if(val==undefined){
			return '您的排名生成中';
		}
		var valLength=val.toString().length;
		var str='0';
		for(var i=0;i<(6-valLength-1);i++){
			str+='0';
		}
		val=str+val;
		return val;
	}
})
//处理手机号中间隐藏
table.filter('Hidden',function(){
	return function(Val){
		if(Val==undefined){
			return '您的排名生成中';
		}
		//var Val=Val.slice(0,3)+"****"+Val.slice(7,11);
		return Val;
	}
})

//手动加载多个ng-app
angular.element(document).ready(
   function (){
    angular.bootstrap(document.getElementById("app"), ["myTable"]);
   }
 );