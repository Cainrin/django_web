(function($){
	H.footer={
		init:function(){
			this.shake();
		},
		shake:function(){
			$('.shake').click(function(){
				var t = simpleTpl();
				t._('<div id="hy_diolag" class="hy_scale">')
					._('<div class="center">')
						._('<em class="shakeimg"><img src="/static/campaigns/picc/mobile/image/fx.png"/></em>')
					._('</div>')
				._('</div>');
				
				$("body").append(t.toString());
				$('#hy_diolag').click(function(){
					$('#hy_diolag').remove();
				})
			})
			
			
		}
	}
	
})(Zepto)
$(function(){
	H.footer.init();
})
