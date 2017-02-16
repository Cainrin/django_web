
$(function(){
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
			var Files='';
			var box_canvas=document.getElementById('box_canvas');
			 var canvas = document.getElementById('canvas');
			var BoxW=box_canvas.offsetWidth;
			//var h=box_canvas.offsetHeight;
		    var h =Math.ceil(window.screen.availHeight);
			canvas.setAttribute("height",h);
			canvas.setAttribute("width",BoxW);
			var photoCanvas = new PhotoCanvas('canvas', BoxW,h, 'loadingImage', document.getElementById("bgImage"));
		    var file = document.getElementById('File');
			file.onchange=function(){
				if(this.files[0].size/1024>5000){
					showTips("请上传图片大小小于5M的图片");
					return false;
				}
				photoCanvas.loadFile(this.files[0]);
				$('.box_img').css('visibility','visible');
				$('.label').hide();
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
			$('#Submit').click(function(){
				Step=$('#step_but').val().trim();
				name=$('#name_but').val().trim();
				phone=$('#phone_but').val().trim();
				if($('.box_img').css('visibility')=='hidden'){
					showTips('请长传图片！');
					return false;
				}
				if(Step==''){
					showTips('请填写步数！');
					return false;
				}
				if(name==''){
					showTips('请填写姓名！');
					return false;
				}
				if(phone==''){
					showTips('请填写手机号！');
					return false;
				}
				$('#step').addClass('none');
				$('#uploadServer').removeClass('none');
				$('.file').addClass('scale')
				
				//-----
			});
			
			$('.upServer').click(function(){
					var formdata = new FormData();
					formdata.append("count",Step);
					formdata.append("workImage",photoCanvas.toImageFile());
					setTimeout(function(){
						$.ajax({
							type:"POST",
							url:"update",
							async:false,
							timeout:'30000',
							data:formdata,
							dataType : "json",
				        	contentType: false,
				        	processData: false,
				        	success:function(response){
				        		console.log('成功')
				        		window.location.href='success?uploadStep='+response.walk;
				        		//localStorage.setItem('money',response.money);
				        		//localStorage.setItem('walk',response.walk);
				        		console.log(response);
				        	},
				        	error:function(err){
				        		console.log('错误')
				        		console.log(err);
				        	}
						});
					},100);
					
					var str='手机号 '+phone+' 姓名 '+name;
            		var data={usrinfo:str};
					$.post('activeusr',data,function(response){
						if(response.result_code==0){
							console.log(response)
						}else{
							console.log('报名失败')
						}
					})
				})
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
