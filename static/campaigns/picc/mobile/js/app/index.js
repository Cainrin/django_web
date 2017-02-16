(function($){
	H.index={
		$bj:document.querySelector('#bj'),
		$text:document.querySelector("#text"),
		$qiqiu:document.querySelector("#qiqiu"),
		$theme:document.querySelector("#theme"),
		init:function(){
			var _this=this;
			var Img=new Image();
			Img.src='/static/campaigns/picc/mobile/image/bj-min.jpg';
			Img.onload=function(){
				_this.bjScroll();
			}
			_this.about();
			
		},
		bjScroll:function(){
			var _this=this;
			var bjW=this.$bj.offsetWidth;
			var WindowW=document.body.offsetWidth;
			var scrollW=bjW-WindowW;
			var textP=_this.$text.querySelectorAll('p');
			var Em=_this.$theme.children;
			textP[0].className='Opacity';
			
			var Time=scrollW/3/100;
			Time=Time.toFixed(1);
			console.log(Time);
			
			var i=0;
			var SetINt;
			function bjSc(){
				SetINt=setInterval(function(){
						i+=3;
						if(i>=scrollW){
							clearInterval(SetINt);
							return false;
						}
						_this.$bj.style.webkitTransform='translateX('+(-i)+'px)';
					//console.log(scrollW)
				},10)
			}
			
			
			$('#play').click(function(){
				//document.getElementById('music').play();	
				textP[0].className='none'
				$(this).addClass('none');
					textP[1].className='Opacity_2';
//				setTimeout(function(){
//				},30)
				setTimeout(function(){
					_this.addEvent(textP[1],'webkitAnimationEnd',function(){
						textP[2].className='Opacity3';
						_this.$qiqiu.style.webkitAnimationPlayState='paused';
						setTimeout(function(){
							textP[2].style.webkitAnimationPlayState='paused';
						},500)
						clearInterval(SetINt);
						$('#play1').removeClass('none');
						$('#play1').click(function(){
							$(this).addClass('none')
							_this.$qiqiu.style.webkitAnimationPlayState='running';
							textP[2].style.webkitAnimationPlayState='running';
							bjSc();
						})
					},false)
				},100)
				bjSc();
				_this.$qiqiu.className='';
				_this.$qiqiu.style.webkitAnimation='TransLate '+Time+'s both linear';
				_this.addEvent(_this.$qiqiu,'webkitAnimationEnd',function(){
					_this.$theme.className='';
					Em[0].className='em1';
					Em[1].className='em2';
					Em[2].className='em3';
					Em[3].className='buts_active em4';
					_this.$qiqiu.querySelectorAll('img')[1].className='';
				})
			})
			
		},
		about:function(){
			$('.buts_active').click(function(){
				var t = simpleTpl();
				t._('<div id="hy_diolag" class="hy_scale">')
					._('<div class="center">')
						._('<em class="active"><img src="/static/campaigns/picc/mobile/image/indexshuom-min.png"/><a class="close_diolag"><img src="/static/campaigns/picc/mobile/image/indexclose-min.png"/></a></em>')
					._('</div>')
				._('</div>');
				
				$("body").append(t.toString());
				$('.close_diolag').click(function(){
					$('#hy_diolag').remove();
				})
			})
			
		},
		addEvent:function(obj,Event,callback){
			obj.addEventListener(Event,callback,false);
		}
	}
})(Zepto);

$(function(){
	H.index.init();
});
