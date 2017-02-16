	var fontSize=document.getElementsByTagName('html')[0];
	var documentW=fontSize.offsetWidth;
	var pw=740;
	fontSize.style.fontSize=100*documentW/pw+"px";

var Day1=1025;
	var Day2=1026;
	var Day3=1027;
	var Day4=1028;
	var Day5=1029;
	var Day6=1030;
	var Day7=1031;
	var Day8=1101;
	var Day9=1102;
	var Day10=1103;
	var Day11=1104;
	var getDate;
	var Dates=new Date();
	var getDateStr=Dates.getDate().toString();
	if(getDateStr.length==1){
		getDate='0'+getDateStr;
	}else{
		getDate=getDateStr;
	}
	var str=(Dates.getMonth()+1)+""+getDate
	//console.log(str)
	//console.log(Dates.getDate())
	 if(Day1>str){
	 	imgSrc="http://hypro-10030008.file.myqcloud.com/mobile/zhonghang/img/start.png"
	 }else if(Day1==str){
	 	imgSrc="http://hypro-10030008.file.myqcloud.com/mobile/zhonghang/img/2016-10-25.png"
	 }else if(Day2==str){
	 	imgSrc="http://hypro-10030008.file.myqcloud.com/mobile/zhonghang/img/2016-10-26.png"
	 }else if(Day3==str){
	 	imgSrc="http://hypro-10030008.file.myqcloud.com/mobile/zhonghang/img/2016-10-27.png"
	 }else if(Day4==str){
	 	imgSrc="http://hypro-10030008.file.myqcloud.com/mobile/zhonghang/img/2016-10-28.png"
	 }else if(Day5==str){
	 	imgSrc="http://hypro-10030008.file.myqcloud.com/mobile/zhonghang/img/2016-10-29.png"
	 }else if(Day6==str){
	 	imgSrc="http://hypro-10030008.file.myqcloud.com/mobile/zhonghang/img/2016-10-30.png"
	 }else if(Day7==str){
	 	imgSrc="http://hypro-10030008.file.myqcloud.com/mobile/zhonghang/img/2016-10-31.png"
	 }else if(Day8==str){
	 	imgSrc="http://hypro-10030008.file.myqcloud.com/mobile/zhonghang/img/2016-11-01.png"
	 }else if(Day9==str){
	 	imgSrc="http://hypro-10030008.file.myqcloud.com/mobile/zhonghang/img/2016-11-02.png"
	 }else if(Day10==str){
	 	imgSrc="http://hypro-10030008.file.myqcloud.com/mobile/zhonghang/img/2016-11-03.png"
	 }else if(Day11==str){
	 	imgSrc="http://hypro-10030008.file.myqcloud.com/mobile/zhonghang/img/2016-11-04.png"
	 }else if(Day11<str){
	 	imgSrc="http://hypro-10030008.file.myqcloud.com/mobile/zhonghang/img/none.png"
	 }
	






var gua = 1,re = 2;  // 可设置刮奖次数
var imgSrc ;

//function showdiv() { 
//	 document.getElementById("bg1").style.display ="block";
//	 document.getElementById("show").style.display ="block";
//}
//
//function hidediv() {
//	 document.getElementById("bg1").style.display ='none';
//	 document.getElementById("show").style.display ='none';
//}

$(function(){
	var width = $("#show_img").width();
	var height = $("#show_img").height();
	var winheight=$(window).height();
	var winwidth=$(window).width();
	//$("#show").css({"width":300+"px","height":160+"px","overflow":"hidden"});
	//$("#show_btn").css({"width":176*0.5+"px","height":76*0.5+"px"});
	//$("#gua_div").html("x"+gua);
	//$("#re_div").html("x"+re);
	
	if(gua == 0){
		showdiv();
	}
})

$(function(){
	var body_width = $(window).width();
	var body_height = $(window).height();
	var height =68;
	var width  =174;
	var bg2_width = $("#bg2_img").width();
	var bg2_height = $("#bg2_img").height();
	
	$("#gua1").css({"margin-top":"0px"});

	//$("#notify").css({"margin-top":"200px"});
	//$("#nImg").width(300).height(101);
	
	//$("#di").css({"margin-top":"50px"});
	//$("#di_img").width(414*0.7).height(24*0.7);


	//$("#gua_div").css({"line-height":width/10+"px","width":width/10+"px","height":width/10+"px","margin-top":"-"+($("#gua").height())+"px","margin-left":$("#gua").height()+5+"px","font-size": $("#gua").height()/1.6+"px"});
	//$("#re").width(width/10).height(width/10);
	//$("#re_div").css({ "line-height":width/10+"px","width":width/10+"px","height":width/10+"px","margin-top":"-"+($("#gua").height())+"px","margin-left":$("#gua").height()+5+"px","font-size": $("#gua").height()/1.6+"px"});
	//$("#front").css({"margin-top":9.3+"px","margin-left":7.5+"px"});
	var gua1_img_width = $("#gua1_img").width();
	if(gua > 0){
		bodys(height,width);
	}
	
	
	
});
function bodys(height,width){
	var img = new Image();         
	var canvas = document.querySelector('canvas');
	//canvas.style.position = 'absolute'; 
	img.addEventListener('load',function(e){  
		var ctx;
		var w = width, h = height;             
		var offsetX = canvas.offsetLeft, offsetY = canvas.offsetTop;  
		//console.log(offsetX)
		var mousedown = false;               
		function layer(ctx){                 
			ctx.fillStyle = 'gray';                 
			ctx.fillRect(0, 0, w, h);             
		}   
		function eventDown(e){                 
			e.preventDefault();                 
			mousedown=true;             
		}   
		function eventUp(e){            
			e.preventDefault();                 
			mousedown=false;             
		}               
		function eventMove(e){                 
			e.preventDefault();                 
			if(mousedown){                     
				if(e.changedTouches){                         
					e=e.changedTouches[e.changedTouches.length-1];                     
				} 
				console.log(document.body.scrollLeft+"---"+document.body.scrollTop+"----"+offsetY)
				var x = (e.clientX + document.body.scrollLeft || e.pageX) - offsetX || 0,                         
				y = (e.clientY + document.body.scrollTop || e.pageY) - offsetY || 0;                     
				with(ctx){                    
					beginPath()                     
					arc(x, y, 15, 0, Math.PI * 2);                         
					fill();                     
				}                
			}             
		}

		canvas.width=w;             
		canvas.height=h; 
		
		canvas.style.backgroundImage='url('+img.src+')'; 
		canvas.style.backgroundSize='100% 100%'
		ctx=canvas.getContext('2d');         
		ctx.fillStyle='b9b9b9';             
		ctx.fillRect(0, 0, w, h);

		layer(ctx);               
		ctx.globalCompositeOperation = 'destination-out';               
		canvas.addEventListener('touchstart', eventDown);             
		canvas.addEventListener('touchend', eventUp);             
		canvas.addEventListener('touchmove', eventMove);             
		canvas.addEventListener('mousedown', eventDown);             
		canvas.addEventListener('mouseup', eventUp);             
		canvas.addEventListener('mousemove', eventMove);       
	});
	
	img.src = imgSrc;
	(document.body.style);
}
//Date.prototype.Format= function(){
//	var d1=new Date("2016/10/25");
//	var d2=new Date("2016/10/26");
//	var d3=new Date("2016/10/27");
//	var d4=new Date("2016/10/28");
//	var d5=new Date("2016/10/29");
//	var d6=new Date("2016/10/30");
//	var d7=new Date("2016/10/31");
//	var d8=new Date("2016/11/01");
//	var d9=new Date("2016/11/02");
//	var d3=new Date("2016/11/03");
//	var d3=new Date("2016/11/04");
//	var d=new Date();
//	alert(d.getFullYear()+"年"+(d.getMonth()+1)+"月"+d.getDate()+"日");
//	
//
//}

	 