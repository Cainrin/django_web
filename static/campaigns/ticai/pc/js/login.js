//用户登录
var login=angular.module('login',[]);
login.controller('log',['$scope','$http','$location',function($scope,$http,$location){
	$scope.Login=function(){
		var username=$scope.username;
		var passwd=$scope.passwd;
		$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
		$http({
			method:'POST',
			url:"login",
			data:$.param({username: username,passwd:passwd}),
			async:false,
			dataType:'json'
		}).success(function(data){
			var code=data.result_code;
			if(code==0){
				sessionStorage.cookie='name_'+username;
				window.location.href='index.html';
			}else{
				$scope.msg=data.result_msg;
			}
			console.log(data)
		}).error(function(data,status){
			console.log(data,status)
		})
	}
}])
