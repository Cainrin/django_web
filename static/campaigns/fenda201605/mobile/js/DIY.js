function start(w,h,W,H,BoxW) {
	 var bg1 = document.getElementById('bg1');
	 
    fabricCustom.loadControlImageObj(document.getElementById("controlImage"));
    var diyCanvas='';
	
    if(W<=320 && H<=480){
    	 diyCanvas= new DIYCanvas('canvas','kit', BoxW, h, 40, 0.4, 'red');
    	 diyCanvas.addKit(bg1,w/20,h/1);
    }
    else if(W<=320 && H<=568){
    	 diyCanvas= new DIYCanvas('canvas','kit',BoxW, h, 40, 0.5, 'red');
    	 diyCanvas.addKit(bg1,w/20,h/1.5);
    }
    else if(W<=375){
    	 diyCanvas= new DIYCanvas('canvas','kit', BoxW, h, 40, 0.7, 'red');
    	 diyCanvas.addKit(bg1,w/10,h/3.4);
    }
    else if(W<=414){
    	 diyCanvas= new DIYCanvas('canvas','kit', BoxW, h, 40, 0.8, 'red');
    	 diyCanvas.addKit(bg1,w/20,h/3.9);
    }
    else if(W<768){
    	 diyCanvas= new DIYCanvas('canvas','kit', BoxW, h, 40,0.9, 'red');
    	 diyCanvas.addKit(bg1,w/24,h/4.5);
    }
    else  if(W>=768){
    	 diyCanvas= new DIYCanvas('canvas','kit', BoxW, h, 40,1, 'red');
    	 diyCanvas.addKit(bg1,w/20,h/3.8);
    }else{
    	diyCanvas= new DIYCanvas('canvas','kit',BoxW, h*0.8, 40, 0.5, 'red');
    	 diyCanvas.addKit(bg1,w/10,h/3.5);
    }
   
     diyCanvas.activate();
    //diyCanvas.toImageFile()
    var pro_canvas = document.getElementById('pro_canvas');
     var pro_img = document.getElementById('pro_img');
 	var final_but = document.getElementById("final_but");
 	var final_img=document.getElementById('final_img');
 	final_but.onclick=function(){
 		diyCanvas.deactivate();
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
					window.location.href="resulted.html?workId="+data.workId;
				},
				error:function(jqXHR){
					alert("数据请求失败，请稍后再试");
					return false;
				}
			});
			
		})
			
}

$(function() {
	var box_canvas=document.getElementById('box_canvas');
	var BoxW=box_canvas.offsetWidth;
    var W =window.screen.availWidth;
    var H =window.screen.availHeight;
    var w =window.screen.availWidth*0.8;
     var h =window.screen.availHeight;
    if(h>568){
    	h =window.screen.availHeight*0.45;
    }else{
    	h =window.screen.availHeight*0.35;
    }
    start(w,h,W,H,BoxW);    
});