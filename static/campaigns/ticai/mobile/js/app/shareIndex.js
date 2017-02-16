
var Openid;
var dataStep=window.location.search.slice(1);
	dataStep=dataStep.split('&');
	for(var i=0;i<dataStep.length;i++){
		var step=dataStep[i].split('=');
		if(step[0]=='Openid'){
			Openid=step[1];
		}
}
$.get('suchAll',{openid:Openid},function(response){
	//alert(JSON.stringify(response))
		if(response.isSelf==0){
			window.location.href='index#/successIndex'
		}
		//alert(JSON.stringify(response))
	})

$(function(){
	$.get('suchAll',{openid:Openid},function(response){
		if(response.isSelf==0){
			window.location.href='index#/successIndex';
			return false;
		}
		$('.step').text(response.count);
		$('.money').text(response.money);
	})
	setTimeout(function(){
		$('html,html img').css('opacity','1');
	},500);
	//alert(Openid)
})
