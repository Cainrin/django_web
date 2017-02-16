
$(function(){
	//var userUplod;
	$.ajax({
		type:"get",
		url:"isnew",
		async:true,
		success:function(response){
			var data=response;
			//alert(JSON.stringify(data));
			if(data.result_code==1){
				//sessionStorage.setItem('userName',data.name);
				//sessionStorage.setItem('userPhone',data.phone);
				$('#name_but').val(data.name);
				$('#phone_but').val(data.phone);
				$('#name_but,#phone_but').attr('disabled',true);
			}
		},
		error:function(er){
			//alert(JSON.stringify(er));
		}
	});
	
	
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
	
	var update={
		init:function(){
			var This=this;
			this.updateFile();
		},
		updateFile:function(){
			//上传照片
			var Files='',FileName=null;
			var box_canvas=document.getElementById('box_canvas');
			 var canvas = document.getElementById('canvas');
			var BoxW=box_canvas.offsetWidth;
			var h=box_canvas.offsetHeight;
		    //var h =Math.ceil(window.screen.availHeight);
			canvas.setAttribute("height",h);
			canvas.setAttribute("width",BoxW);
			var photoCanvas = new PhotoCanvas('canvas', BoxW,h, 'loadingImage', document.getElementById("bgImage"));
		    var file = document.getElementById('File');
			file.onchange=function(){
				if(this.files[0].size/1024>5000){
					showTips("请上传图片大小小于5M的图片");
					return false;
				}
				FileName=this.files[0];
				photoCanvas.loadFile(this.files[0]);
				$('.box_img').css('visibility','visible');
				//$('.label').hide();
				$('.back').show();
			}
//			//返回重新上传
//			$('.back').click(function(){
//				$('.box_img').css('visibility','hidden');
//				$('.label').show();
//				$('.back').hide();
//			});
			//点击上传
			var Step,name,phone;
			//var ph=/^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1})|(17[0-9]{1}))+\d{8})$/;
			var ph=/^1(3|4|5|7|8)\d{9}$/;
			$('#Submit').click(function(){
				Step=$('#step_but').val().trim();
				name=$('#name_but').val().trim();
				phone=$('#phone_but').val().trim();
				if($('.box_img').css('visibility')=='hidden'){
					showTips('请上传图片！');
					return false;
				}
				if(Step==''){
					showTips('请填写步数！');
					return false;
				}
				if(Step>30000){
					showTips('步数不能大于3万');
					return false;
				}
				//if(name!='' || phone!=''){
					if(name==''){
						showTips('请填写姓名！');
						return false;
					}
					if(phone==''){
						showTips('请填写手机号！');
						return false;
					}
					if(!ph.test(phone)){
						showTips('请填写正确的手机号');
						return false;
					}
					
				//}
				$('#step').addClass('none');
				$('#uploadServer').removeClass('none');
				$('.file').addClass('scale')
				$('.label').hide();
				//-----
			});
			
			$('.upServer').click(function(){
					//var formdata = new FormData();
					//formdata.append("count",Step);
					//formdata.append("workImage",photoCanvas.toImageFile());
					
					
					var geshi=FileName.type.split('/')[1];
					var imgNmae=Date.parse(new Date())/1000;
					var bucketName = "ticai";
					var cos = new CosCloud("10030008");
					console.log(FileName)
					cos.uploadFile(function(result){
						//console.log("成功"+result);
						var jsonData=JSON.parse(result);
						var dataUrl=jsonData.data;
						$.post('update',{
							count:Step,
							img:dataUrl.source_url,
						},function(response){
							//alert(JSON.stringify(response))
							//console.log(response);
							//alert(JSON.stringify(response))
							if(response.result_code==1){
				        			showTips(response.result_msg);
				        			return false;
				        		}
				        		var walk=response.walk;
				        		//console.log('上传成功')
			            		if(name!=''){
					        		var str='手机号 '+phone+' 姓名 '+name;
				            		var data={usrinfo:str};
				            		//console.log(data)
			            			$.post('activeusr',data,function(responses){
										if(responses.result_code==0){
											console.log(responses)
											window.location.href='success?uploadStep='+walk;
										}else{
											console.log('报名失败')
										}
									})
			            		}else{
			            			window.location.href='success?uploadStep='+walk;
			            		}
						})
						
					}, function(err){
						showTips('上传失败')
		        		//alert(JSON.stringify(err))
		        		console.log('错误')
		        		console.log(err);
					}, bucketName, "/"+imgNmae+"."+geshi, photoCanvas.toImageFile());
				
				});
				
					
//					setTimeout(function(){
//						$.ajax({
//							type:"POST",
//							url:"update",
//							async:false,
//							timeout:'30000',
//							data:formdata,
//							dataType : "json",
//				        	contentType: false,
//				        	processData: false,
//				        	success:function(response){
//				        		//alert(JSON.stringify(response))
//				        		if(response.result_code==-1){
//				        			showTips('上传失败');
//				        			return false;
//				        		}
//				        		var walk=response.walk;
//				        		console.log('上传成功')
//			            		if(name!=''){
//					        		var str='手机号 '+phone+' 姓名 '+name;
//				            		var data={usrinfo:str};
//			            			$.post('activeusr',data,function(responses){
//										if(responses.result_code==0){
//											window.location.href='success?uploadStep='+walk;
//										}else{
//											console.log('报名失败')
//										}
//									})
//			            		}else{
//			            			window.location.href='success?uploadStep='+walk;
//			            		}
//								
//				        		//localStorage.setItem('money',response.money);
//				        		//localStorage.setItem('walk',response.walk);
//				        	},
//				        	error:function(err){
//				        		showTips('上传失败')
//				        		//alert(JSON.stringify(err))
//				        		console.log('错误')
//				        		console.log(err);
//				        	}
//						});
//					},100);
					
					
				//})
			$('.cancel').click(function(){
				$('#step').removeClass('none');
				$('#uploadServer').addClass('none');
				$('.file').removeClass('scale');
				$('.box_img').css('visibility','hidden');
				$('.label').show();
				$('.back').hide();
				photoCanvas.clearCanvas();
			});
			
		}
	}
	update.init();
})
