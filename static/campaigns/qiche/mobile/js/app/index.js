
$(function(){
	var main_wrap=document.getElementById('main_wrap');
	var envelope=document.querySelector('#envelope');
	var envelope1=document.querySelector('#envelope1');
	var Enve=document.querySelector('#Enve');
	var shake=document.querySelector('#shake');
	setTimeout(function(){
		main_wrap.style.webkitTransition='all 1s';
		envelope.style.webkitTransition='all 1s';
		envelope1.style.webkitTransition='all 1s';
	},500)

	function Shake(){
			main_wrap.className='mainAnim';
			envelope.className='envelope';
			envelope1.className='envelope';
		}
	shake.onclick=function(){
		Shake()
	}
	Enve.onclick=function(){
		main_wrap.className='';
		envelope.className='';
		envelope1.className='';
	}
})



