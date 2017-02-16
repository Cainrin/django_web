(function($){
	H.list={
		$listBut:document.querySelector('.list_but'),
		$list:document.querySelector('#list'),
		$pd:true,
		$trans:0,
		init:function(){
			var _this=this;
			_this.leftScroll();
		},
		leftScroll:function(){
			var arr=[
					{
						id:1,
						title:'书包',
						url:'1-min.png'
					},
					{
						id:2,
						title:'水彩笔',
						url:'2-min.png'
					},
					{
						id:3,
						title:'自行车',
						url:'3-min.png'
					},
					{
						id:4,
						title:'足球',
						url:'4-min.png'
					},
					{
						id:5,
						title:'运动鞋',
						url:'5-min.png'
					},
					{
						id:6,
						title:'洋娃娃',
						url:'6-min.png'
					},
					{
						id:7,
						title:'台灯',
						url:'7-min.png'
					},
					{
						id:8,
						title:'羽绒服',
						url:'8-min.png'
					},
					{
						id:9,
						title:'新华字典',
						url:'9-min.png'
					},
					{
						id:10,
						title:'录音播放机',
						url:'10-min.png'
					},
					{
						id:11,
						title:'望远镜',
						url:'11-min.png'
					},
					{
						id:12,
						title:'手表',
						url:'12-min.png'
					},
					{
						id:13,
						title:'地球仪',
						url:'13-min.png'
					},
					{
						id:14,
						title:'雨伞',
						url:'14-min.png'
					},
					{
						id:15,
						title:'风筝',
						url:'15-min.png'
					},
					{
						id:16,
						title:'棉被',
						url:'16-min.png'
					},
					{
						id:17,
						title:'雨鞋',
						url:'17-min.png'
					}
				]
			var _this=this;
			var t = simpleTpl();
			//var num=Math.ceil(arr.length/5);
			var h=0;
			
			$.post('dream',function(response){
				var data=response.dreamList;
				var liNum=[5,3,4,5]
				var num=Math.ceil(data.length/5);
				for(i=0;i<num;i++){
					//console.log(arr[i].id)
					t._('<li class="li_'+i+'">')
						for(var k=0;k<liNum[i];k++){
							try{
								if(arr[h].id=='undefined'){
									return false;
								}
								t._('<em data-id='+(arr[data[h].id-1].id)+'><img src="/static/campaigns/picc/mobile/image/x/'+arr[data[h].id-1].url+'"/><span>'+arr[data[h].id-1].title+'</span></em>');
								h=h+1;
							}catch(e){
								//TODO handle the exception
							}
						}
					t._('</li>')
				}
				
				$('#list').append(t.toString())
				$('#list em').click(function(){
					var Id=$(this).data('id');
					window.location.href='main.html?arrId='+Id;
				})
				var li_length=_this.$list.children;
				//console.log(li_length.length);
				for(var j=0;j<li_length.length;j++){
					li_length[j].style.width=100/li_length.length+"%";
				}
				_this.$list.style.width=li_length.length*100+'%';
				_this.$listBut.onclick=function(){
					//_this.removeEvent(_this.$list,'transitionend',function(){})
					if(_this.$pd){
						var i=0;
						_this.$pd=false;
	//					if(i>=li_length.length){
	//						return false;
	//					}
						_this.$list.className='trn';
						var Time=setInterval(function(){
							i+=5;
							if(i>=100){
								clearInterval(Time);
								_this.$pd=true;
								var liChildren=_this.$list.children;
								console.log(liChildren)
								var removeChild=_this.$list.removeChild(liChildren[0])
								_this.$list.appendChild(removeChild);
								_this.$list.style.left="0%";
								
								return false;
							}
							_this.$list.style.left=-i+"%";
						},30)
					}
					
				}
			});	
			
			
		},
		addEvent:function(obj,Event,callback){
			obj.addEventListener(Event,callback,false);
		},removeEvent:function(obj,Event,callback){
			obj.removeEventListener(Event,callback,false);
		}
	}
})(Zepto)
$(function(){
	H.list.init();
})
