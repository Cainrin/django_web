//右侧路由控制
var table=angular.module('myTable',['ngRoute']);
table.config(function($routeProvider){
	$routeProvider.when('/',{
		templateUrl:'view/index.html',
		controller:'Index'
	})
	.when('/successIndex',{
		templateUrl:'view/indexSuccess.html',
		controller:'successIndex'
	}).when('/list',{
		templateUrl:'view/list.html',
		controller:'List'
	})
	.when('/prize',{
		templateUrl:'view/prize.html',
		controller:'Prize'
	})
	.when('/signUp',{
		templateUrl:'view/signUp.html',
		controller:'SignUp'
	})
	.when('/explain',{
		templateUrl:'view/explain.html',
		//controller:'Explain'
	})
	.otherwise({
		redirectTo:'/'
	})
});

//手动加载多个ng-app
angular.element(document).ready(
   function (){
    angular.bootstrap(document.getElementById("app"), ["myTable"]);
   }
 );