(function($){
	H.main={
		CookieVote:$.fn.cookie('CookieVote'),
		init:function(){
			var _this=this;
			this.swipt();
		},
		swipt:function(){
			var _this=this;
			var t = simpleTpl();
			var arr=[
				{
					id:1,
					text:'开学我就五年级了</br>书更多了，好想有个大点的书包</br>继续装着我的梦想',
					url:'1.png',
					header:'罗同学和余同学',
				},
				{
					id:2,
					text:'我想用水彩笔画出更加多彩的世界</br>有青山绿树、蓝天白云</br>还有群星闪烁',
					url:'2.png',
					header:'黄同学和雷同学',
				},
				{
					id:3,
					text:'有了自行车</br>就再也不用天还没亮</br>就出门上学了',
					url:'3.png',
					header:'徐同学和巨同学',
				},
				{
					id:4,
					text:'翻着毛边的旧皮球越来越瘪</br>有个足球，课间就能和同学们</br>在操场上一起踢了',
					url:'4.png',
					header:'蒲同学和秦同学',
				},
				{
					id:5,
					text:'有双运动鞋</br>走山路和上体育课</br>就会比布鞋轻松多了',
					url:'5.png',
					header:'赵同学和吴同学',
				},
				{
					id:6,
					text:'妈妈外出打工</br>有只洋娃娃</br>我就能抱着它安心入睡',
					url:'6.png',
					header:'赵同学和李同学',
				},
				{
					id:7,
					text:'一直都梦想着</br>能有一盏明亮的台灯</br>这样或许就不用在昏暗的灯光下写作业了',
					url:'7.png',
					header:'张同学和高同学',
				},
				{
					id:8,
					text:'山里的冬天很冷</br>我也好想像城里的小朋友那样</br>能有件厚厚的羽绒服',
					url:'8.png',
					header:'童同学和巨同学',
				},
				{
					id:9,
					text:'图书角的新华字典我们都很爱惜</br>但因为只有一本大家用的太多</br>所以书角都已卷起',
					url:'9.png',
					header:'巨同学和陈同学',
				},
				{
					id:10,
					text:'很喜欢老师那台录音机里播放的</br>课文朗读声</br>如果我在家也可以听到就好了',
					url:'10.png',
					header:'罗同学和李同学',
				},
				{
					id:11,
					text:'我很喜欢夜空</br>一直梦想着长大能成为天文学家</br>有了望远镜，我就能好好看看天上的星星啦',
					url:'11.png',
					header:'罗同学和周同学',
				},
				{
					id:12,
					text:'我想有一块粉色的手表</br>提醒自己珍惜时间</br>好好学习',
					url:'12.png',
					header:'姜同学和杨同学',
				},
				{
					id:13,
					text:'老师的地球仪每次都很抢手</br>如果我也有一个，肯定会爱不释手</br>天天转动去“寻找世界”',
					url:'13.png',
					header:'杨同学和蒲同学',
				},
				{
					id:14,
					text:'我想家里添一把雨伞</br>家里的伞柄已经断了一小截</br>可爷爷还是用这着它，舍不得扔',
					url:'14.png',
					header:'王同学和李同学',
				},
				{
					id:15,
					text:'今年春天爸爸做了纸风筝，我跟弟弟都很开心</br>如果有一只五彩的蝴蝶风筝</br>一定会飞的更高',
					url:'15.png',
					header:'陈同学和李同学',
				},
				{
					id:16,
					text:'冬天睡觉，我们都将所有棉袄盖在被子上</br>重重的但确实暖和很多</br>盼望能有新的棉被，给我跟妹妹更多的温暖',
					url:'16.png',
					header:'陈同学和巨同学',
				},
				{
					id:17,
					text:'山里经常下雨</br>有双雨鞋</br>放学上学路上就方便多了',
					url:'17.png',
					header:'江同学和巨同学',
				}
			];
			var Max=10000;
			$.post('dream',function(response){
				var data=response.dreamList;
				var  arrId=getQueryString('arrId');
				var iNum=0,day=27;
				var newDay=new Date().getDate();
				for(i=0;i<data.length;i++){
					if(arrId==data[i].id){
						iNum=i;
						dataSlice=data.splice(0,iNum);
						data=data.concat(dataSlice);
					}
				}
			for(var j = 0; j<data.length;j++){
				if(data[j].votecount>Max && day>newDay){
					data[j].votecount=Max-7;
				}else if(data[j].votecount<Max && day<=newDay){
					data[j].votecount=Max;
				}
				t._('<div class="swiper-slide" data-id='+data[j].id+'>')
					._('<header class='+(data[j].votecount<Max?'':'none')+'>')
						._('<p>已有<span class="vote_span1"><i>'+data[j].votecount+'</i><em class="add_1">+1</em></span>人点亮<span>'+arr[data[j].id-1].header+'的愿望</span></p>')
						._('<p>等你继续来助力</p>')
					._('</header>')
					._('<header class='+(data[j].votecount>=Max?'':'none')+'>')
						._('<p>'+arr[data[j].id-1].header+'的心愿已被<span class="vote_span2">'+data[j].votecount+'</span>位爱心之人点亮</p>')
						._('<p>江苏人保会将把礼物送到孩子手上</p>')
						._('<p>请用你的好意助力其他愿望</p>')
					._('</header>')
					._('<em  class="xtu"><img    src="/static/campaigns/picc/mobile/image/big/'+arr[data[j].id-1].url+'"    class='+(data[j].votecount>=Max?'':'brightness')+' /></em>')
					._('<div class="text">'+arr[data[j].id-1].text+'</div>')
				._('</div>');
			}
		//t._('</div>');
			$(".swiper-wrapper").html(t.toString());
			var mySwiper = new Swiper('.swiper-container',{
					    pagination: '.pagination',
					    loop:true,
					    grabCursor: true,
					    paginationClickable: true,
					  });
			
			mySwiper.wrapperTransitionEnd(function(){
				 butVote()
			},true)
			 $('.arrow-left').on('click', function(e){
					    e.preventDefault()
					    mySwiper.swipePrev()
					  })
			  $('.arrow-right').on('click', function(e){
			    e.preventDefault()
			    mySwiper.swipeNext()
			  })
			//点击投票
			function butVote(){
				var activeNum=parseInt($('.swiper-slide-active .vote_span1 i').text());
				if(activeNum>=Max || $.fn.cookie('CookieVote2')){
					$('.disVote').removeClass('none');
					$('.vote').addClass('none');
				}else{
					$('.vote').removeClass('none');
					$('.disVote').addClass('none');
				}
			}
			
			function yd(){
				var t = simpleTpl();
					t._('<div id="hy_diolag" class="hy_scale">')
						._('<div class="center">')
							._('<div class="vote_bj">')
								._('<i><img src="/static/campaigns/picc/mobile/image/9-21-min.png"/></i>')
								._('<p>感谢您付出的爱心<br/>您仅有的一次助力机会已经用完</p>')
								._('<p>')
								._('<span class="close1"><img src="/static/campaigns/picc/mobile/image/9-20X-min.png"/></span>')
								._('</p>')
							._('</div>')
						._('</div>')
					._('</div>');
					
					$("body").append(t.toString());
					$('.close1').click(function(){
						$('#hy_diolag').remove();
					});
			}
			butVote();
			$('.disVote').click(function(){
				yd();
			})
			
			$('.vote').click(function(){
				var Id=$('.swiper-slide-active').attr('data-id');
				var t = simpleTpl();
				t._('<div id="hy_diolag" class="hy_scale">')
					._('<div class="center">')
						._('<div class="vote_bj">')
							._('<p>您确认用仅有的一次机会<br/>为这位孩子点亮心愿吗?</p>')
							._('<p><a class="submit"><img src="/static/campaigns/picc/mobile/image/submit-min.png"/></a>')
							._('<a class="close"><img src="/static/campaigns/picc/mobile/image/close-min.png"/></a>')
							._('</p>')
						._('</div>')
					._('</div>')
				._('</div>');
				
				$("body").append(t.toString());
				$('.close').click(function(){
					$('#hy_diolag').remove();
				});
				
				$('.submit').click(function(){
					$.post('vote',{id:Id},function(response){
						if(response.result_code){
							//$.fn.cookie('CookieVote','ok',{expires: 30 });
							//yd();
							//return false;
						};
						$('#hy_diolag').remove();
						$.fn.cookie('CookieVote','ok',{ expires: 30 });
						
						butVote();
						setTimeout(function(){
							$('#hy_diolag').remove();
							$('.swiper-slide-active .xtu').addClass('shan');
						},500);
						setTimeout(function(){
							$('.swiper-slide-active .add_1').addClass('addem');
							setTimeout(function(){
								$('.swiper-slide-active .vote_span1 i').text((parseInt($('.swiper-slide-active .vote_span1 i').text())+1));
								if(parseInt($('.swiper-slide-active .vote_span1 i').text())>=Max){
									$('.swiper-slide-active .xtu img').remove('brightness')
								}
							},800)
						},1000)
						setTimeout(function(){
							window.location.href='footer.html';
						},3000)
					})
				})
				
			})
		});	
	}
			
		
	}
})(Zepto)
$(function(){
	H.main.init();
})