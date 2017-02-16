
function start() {
    var w =310 || window.screen.availWidth;
    var h =425 || window.screen.availHeight;
    var bg1 = document.getElementById('bg1');
    fabricCustom.loadControlImageObj(document.getElementById("controlImage"));
     var diyCanvas = new DIYCanvas('canvas', 'kit', w, h, 50, 1, 'red');
    diyCanvas.addKit(bg1,30,55);
    diyCanvas.activate();
  
    var pro_canvas = document.getElementById('pro_canvas');
     var pro_img = document.getElementById('pro_img');
 	var final_but = document.getElementById("final_but");
 	var final_img=document.getElementById('final_img');
 	var i=0;
	$('.overview li').click(function(){
		i++;
		console.log(i)
	})
	$('.reset_but').click(function(){
		$('.reset_but').addClass("none");
		$('#box2').addClass('none');
		$('#box1').removeClass('none');
		$('.sub2').addClass('none');
		$('.sub1').removeClass('none');
		$('#pro_canvas').show();
		$("#pro_img").hide();
		
	})
	//点击出现弹层
		$('.sub1').bind('click',function(){
			if(i==0){
				Diolag('.dialog_wrap',"请至少选择一项制作元素")
				return false;
			}else{
				$('.reset_but').removeClass("none");
				$('#box2').removeClass('none');
				$('#box1').addClass('none');
				$('.sub2').removeClass('none');
				$('.sub1').addClass('none');
			}
			
		})
 	
 	final_but.onclick=function(){
 		if(i==0){
 			return false;
 		}
 		
 		diyCanvas.deactivate();
 		final_img.className='';
 		pro_canvas.style.display="none";
 		pro_img.style.display="block";
		final_img.src = diyCanvas.toImageSrc();
 	}
 	
 	
 	//cookie设置
	function setCookie(name,value){ 
	　　var exp = new Date(); 
	　　exp.setTime(exp.getTime() + 1*60*60*1000);//有效期1小时 
	　　document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString(); 
	}
	
	function getCookie(name){
	　　var arr = document.cookie.match(new RegExp("(^| )"+name+"=([^;]*)(;|$)"));
	　　if(arr != null)　　　　
	　　　　return unescape(arr[2]);
	　　return null;
	}
		
	if(getCookie('name')){
		$('.name').val(getCookie('name'))
	}
	if(getCookie('phone')){
		$('.phone').val(getCookie('phone'))
	}
 	
	$('.sub2').click(function(){
		
			var Name=$('.name').val().trim();
			var Phone=$('.phone').val().trim();
			var WorkName=$('.workName').val().trim();
			var Yx=$('.yx').val().trim();
			if(Name==""){
				Diolag('.dialog_wrap',"请填写姓名")
				return false;
			}
			setCookie("name",Name);
			var ph=/^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$/;
			if(!ph.test(Phone)){
				Diolag('.dialog_wrap',"手机号码不能为空或填写不正确")
				return false;
			}
			setCookie("phone",Phone);
			if(WorkName==""){
				Diolag('.dialog_wrap',"请填写作品名")
				return false;
			}
			if(Yx==""){
				Diolag('.dialog_wrap',"请填写院校名")
				return false;
			}
			var formdata = new FormData();
			
			formdata.append("authorName",Name);
			formdata.append("authorCellphone",Phone)
			formdata.append("workName",WorkName)
			formdata.append("authorSchool",Yx);
			formdata.append("workImage",diyCanvas.toImageFile());
			
			$.ajax({
				type : 'POST',
				async : false,
				url : "uploadDIYWork",
				data:formdata,
				dataType : "json",
	        	contentType: false,
	        	processData: false,
				success : function(data) {
					window.location.href="details.html?workId="+data.workId;
				},
				error:function(jqXHR){
					if(jqXHR.status==400){
						alert(jqXHR.status+":"+jqXHR.responseJSON.errorMessage);
						return false;
					}
					if(jqXHR.status==404){
						alert(jqXHR.status+":"+jqXHR.responseJSON.errorMessage);
						return false;
					}
					if(jqXHR.status==500){
						alert(jqXHR.status+":"+jqXHR.responseJSON.errorMessage);
						return false;
					}
					if(jqXHR.status==501){
						alert(jqXHR.status+":"+jqXHR.responseJSON.errorMessage);
						return false;
					}
					alert("数据请求失败，请稍后再试");
					return false;
				}
			});
			
		})
    
}

$(function() {
//  var image = new Image();
//  image.onload = function() {
//      fabricCustom.loadImageObj(this);
//      start();
//  };
//  image.src = "img/control.png";        
start();
});