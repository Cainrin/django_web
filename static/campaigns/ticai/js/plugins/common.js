var __ns = function( fullNs ) {
    var nsArray = fullNs.split( '.' );
    var evalStr = '';
    var ns = '';
    for ( var i = 0, l = nsArray.length; i < l; i++ ) {
        i !== 0 && ( ns += '.' );
        ns += nsArray[i];
        evalStr += '( typeof ' + ns + ' === "undefined" && (' + ns + ' = {}) );';
    }
    evalStr !== '' && eval( evalStr );
}
var __noop = function() {};
var W = W || window;
__ns('H');


// 从data_collect.js转移过来的
var recordUserLog = function(openid, operateDesc, operateDomId, loadingTime, flag) {
	$.ajax({
		type : "get",
		async : false,
		url : domain_url + "api/common/reportlog",
		dataType : "jsonp",
		jsonp : "callback",
		jsonpCallback : "commonReportlogHandler",
		data : {
			openid : openid,
			operateDesc : encodeURIComponent(operateDesc),
			operateDomId : operateDomId,
			loadingTime : loadingTime,
			from : gefrom,
			flag : flag
		}
	});
}
/**
 * 记录用户操作日志
 * 
 * @param openid 操作用户的openid
 * @param operateDesc 中文描述做的事情
 * @param operateDomId 操作的元素的id
 */
var recordUserOperate = function(openid, operateDesc, operateDomId) {
	recordUserLog(openid, operateDesc, operateDomId, "", "false");
}
/**
 * 加载页面记录日志
 * 
 * @param openid 操作用户的openid
 * @param operateDesc 进入的某页面名称
 * @param loadingTime 页面加载耗时多少毫秒
 */
function recordUserPage(openid, operateDesc, loadingTime) {
	recordUserLog(openid, operateDesc, "", loadingTime, "true");
}
// 从data_collect.js转移过来的 end

var callbackUserSaveHandler = function(data) {};
var getQueryString = function( name ) {
    var currentSearch = decodeURIComponent( location.search.slice( 1 ) );
    if ( currentSearch != '' ) {
        var paras = currentSearch.split( '&' );
        for ( var i = 0, l = paras.length, items; i < l; i++ ) {
            items = paras[i].split( '=' );
            if ( items[0] === name) {
                return items[1];
            }
        }
        return '';
    }
    return '';
};

var from = getQueryString("from");
var gefrom = from || getQueryString("gefrom");
var cb41faa22e731e9b = getQueryString("cb41faa22e731e9b");
var toUrl = function(url) {
	showLoading();
	if (from != null && from != '') {
		if (url.indexOf(".html?") > 0) {
			url = url + "&gefrom=" + from;
		} else {
			url = url + "?gefrom=" + from;
		}
	};
	if (gefrom != null && gefrom != '') {
		if (url.indexOf("gefrom=") < 0) {
			if (url.indexOf(".html?") > 0) {
				url = url + "&gefrom=" + gefrom;
			} else {
				url = url + "?gefrom=" + gefrom;
			}
		}
	};
	var delay = Math.ceil(1500*Math.random() + 500);
	setTimeout(function(){window.location.href = url}, delay);
};

var getResult = function(url, data, callback, showloading, $target, isAsync) {
	data.dev="tv_jiangsu_love";
	if (showloading) {
		showLoading($target);
	}
	$.ajax({
		type : 'GET',
		async : typeof isAsync === 'undefined' ? false : isAsync,
		url : domain_url + url,
		data: data,
		dataType : "jsonp",
		jsonp : callback,
		complete: function() {
			if (showloading) {
				hideLoading($target);
			}
		},
		success : function(data) {}
	});
};
//將毫秒轉化為yyyy-MM-dd HH:mm:ss格式的日期
var  timeTransform = function(TimeMillis){
	  
	var data = new Date(TimeMillis);
    var year = data.getFullYear();  //获取年
    var month = data.getMonth()>=9?(data.getMonth()+1).toString():'0' + (data.getMonth()+1);//获取月
    var day = data.getDate()>9?data.getDate().toString():'0' + data.getDate(); //获取日
    var hours = data.getHours()>9?data.getHours().toString():'0' + data.getHours();
    var minutes = data.getMinutes()>9?data.getMinutes().toString():'0' + data.getMinutes();
    var ss = data.getSeconds()>9?data.getSeconds().toString():'0' + data.getSeconds();
    var time = year + "-" + month + "-" + day + " " + hours + ":" + minutes + ":"+ ss;
    return time;
};

var  timeTransformDay = function(TimeMillis){
	var data = new Date(TimeMillis);
    var year = data.getFullYear();  //获取年
    var month = data.getMonth()>=9?(data.getMonth()+1).toString():'0' + (data.getMonth()+1);//获取月
    var day = data.getDate()>9?data.getDate().toString():'0' + data.getDate(); //获取日
    var hours = data.getHours()>9?data.getHours().toString():'0' + data.getHours();
    var minutes = data.getMinutes()>9?data.getMinutes().toString():'0' + data.getMinutes();
    var ss = data.getSeconds()>9?data.getSeconds().toString():'0' + data.getSeconds();
    var time = year+""+month+""+day+"";
    return time;
};
var jsArrSort = function(obj){
	obj.sort( function(a, b){   
	    return parseInt(a["px" ]) > parseInt(b["px" ]) ? 1 : parseInt(a[ "px"]) == parseInt(b[ "px" ]) ? 0 : -1;   
	}); 
	return obj;
}
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
var simpleTpl = function( tpl ) {
    tpl = $.isArray( tpl ) ? tpl.join( '' ) : (tpl || '');

    return {
        store: tpl,
        _: function() {
            var me = this;
            $.each( arguments, function( index, value ) {
                me.store += value;
            } );
            return this;
        },
        toString: function() {
            return this.store;
        }
    };
};

var normalDate = function(stamp, format, zero) {
    var stamp = Number(stamp),
    date = new Date(stamp), formatDate,
    format = format ? format : "yyyy-mm-dd hh:ii:ss",
    zero = (zero === undefined) ? true : zero,
    dateNum = function(num) { return num < 10 ? '0' + num : num; },
    _d = zero ? dateNum : function(s){return s;};

	var year = _d(date.getFullYear()),
	    month = _d(date.getMonth() + 1),
	    day = _d(date.getDate()),
	    hour = _d(date.getHours()),
	    minute = _d(date.getMinutes()),
	    second = _d(date.getSeconds());
	
	formatDate = format.replace(/yyyy/i, year).replace(/mm/i, month).replace(/dd/i, day)
	            .replace(/hh/i, hour).replace(/ii/i, minute).replace(/ss/i, second);
	return formatDate;
};

var share = function(backUrl) {
	var t = simpleTpl(),
		$share_box = $('#share-box');
	
	if ($share_box.length == 0) {
		t._('<div class="share-box" id="share-box"></div>');
		$share_box = $(t.toString());
		$share_box.click(function(e) {
			$(this).hide();
		});
		$('body').append($share_box);
	} else {
		$share_box.show();
	}
};

var str2date = function(str) {
	str = str.replace(/-/g, '/');
	return new Date(str);
};

var timestamp = function(str) {
	var timestamp = Date.parse(str2date(str));
	return timestamp / 1000;
};

// yyyy年MM月dd日 hh:mm:ss
var dateformat = function(date, format) {
	var z = {
		M : date.getMonth() + 1,
		d : date.getDate(),
		h : date.getHours(),
		m : date.getMinutes(),
		s : date.getSeconds()
	};
	format = format.replace(/(M+|d+|h+|m+|s+)/g, function(v) {
		return ((v.length > 1 ? "0" : "") + eval('z.' + v.slice(-1))).slice(-2);
	});
	return format.replace(/(y+)/g, function(v) {
		return date.getFullYear().toString().slice(-v.length)
	});
}

var dateNum = function(num) {
	return num < 10 ? '0' + num : num;
};

var showLoading = function($container) {
	var t = simpleTpl(),
		$container = $container || $('body'),
		$spinner = $container ? $container.find('#spinner') : $('body').children('#spinner');
	
	if ($spinner.length > 0) {
		$spinner.show();
	} else {
		t._('<div id="spinner" class="spinner">')
			._('<div class="spinner-wrapper">')
			  ._('<div class="spinner-container container1">')
			    ._('<div class="circle1"></div>')
			    ._('<div class="circle2"></div>')
			    ._('<div class="circle3"></div>')
			    ._('<div class="circle4"></div>')
			  ._('</div>')
			  ._('<div class="spinner-container container2">')
			    ._('<div class="circle1"></div>')
			    ._('<div class="circle2"></div>')
			    ._('<div class="circle3"></div>')
			    ._('<div class="circle4"></div>')
			  ._('</div>')
			  ._('<div class="spinner-container container3">')
			    ._('<div class="circle1"></div>')
			    ._('<div class="circle2"></div>')
			    ._('<div class="circle3"></div>')
			    ._('<div class="circle4"></div>')
			  ._('</div>')
		  ._('</div>')
		._('</div>');
		
		var width = $(window).width(),
			height = $(window).height(),
			spinnerSize = 50;
		$spinner = $(t.toString()).css({'left': (width - spinnerSize) / 2, 'top': (height - spinnerSize) / 2});
		$container.append($spinner);
	}
};

var hideLoading = function($container) {
	if ($container) {
		$container.find('.spinner').hide();
	} else {
		$('body').children('.spinner').hide();
	}
	$('.copyright').removeClass('hidden');
};

var imgReady = (function () {
    var list = [], intervalId = null,

    // 用来执行队列
    tick = function () {
        var i = 0;
        for (; i < list.length; i++) {
            list[i].end ? list.splice(i--, 1) : list[i]();
        }
        ;
        !list.length && stop();
    },

    // 停止所有定时器队列
    stop = function () {
        clearInterval(intervalId);
        intervalId = null;
    };

    return function (url, ready, load, error) {
        var onready, width, height, newWidth, newHeight,
            img = new Image();

        img.src = url;

        // 如果图片被缓存，则直接返回缓存数据
        if (img.complete) {
            ready.call(img);
            load && load.call(img);
            return;
        }
        ;

        width = img.width;
        height = img.height;

        // 加载错误后的事件
        img.onerror = function () {
            error && error.call(img);
            onready.end = true;
            img = img.onload = img.onerror = null;
        };

        // 图片尺寸就绪
        onready = function () {
            newWidth = img.width;
            newHeight = img.height;
            if (newWidth !== width || newHeight !== height ||
                // 如果图片已经在其他地方加载可使用面积检测
                newWidth * newHeight > 1024
                ) {
                ready.call(img);
                onready.end = true;
            }
            ;
        };
        onready();

        // 完全加载完毕的事件
        img.onload = function () {
            // onload在定时器时间差范围内可能比onready快
            // 这里进行检查并保证onready优先执行
            !onready.end && onready();

            load && load.call(img);

            // IE gif动画会循环执行onload，置空onload即可
            img = img.onload = img.onerror = null;
        };

        // 加入队列中定期执行
        if (!onready.end) {
            list.push(onready);
            // 无论何时只允许出现一个定时器，减少浏览器性能损耗
            if (intervalId === null) intervalId = setInterval(tick, 40);
        };
    };
})();

var add_param = function(sourceUrl, parameterName, parameterValue, replaceDuplicates) {
	if ((sourceUrl == null) || (sourceUrl.length == 0)) {
		sourceUrl = document.location.href;
	}
	var urlParts = sourceUrl.split("?");
	var newQueryString = "";
	if (urlParts.length > 1) {
		var parameters = urlParts[1].split("&");
		for ( var i = 0; (i < parameters.length); i++) {
			var parameterParts = parameters[i].split("=");
			if (!(replaceDuplicates && parameterParts[0] == parameterName)) {
				if (newQueryString == "") {
					newQueryString = "?";
				} else {
					newQueryString += "&";
				}
				newQueryString += parameterParts[0] + "=" + parameterParts[1];
			}
		}
	}
	
	if (parameterValue !== null) {
		if (newQueryString == "") {
			newQueryString = "?";
		} else {
			newQueryString += "&";
		}
		newQueryString += parameterName + "=" + parameterValue;
	}
	return urlParts[0] + newQueryString;
}

//beginTime,endTime  yy-mm-dd hh:mm:ss
//return -1   beginTime > endTime
//return 0    beginTime = endTime
//return 1    beginTime < endTime
function comptime(beginTime, endTime){
    var beginTimes=beginTime.substring(0,10).split('-');  
    var endTimes=endTime.substring(0,10).split('-');  
    beginTime=beginTimes[1]+'-'+beginTimes[2]+'-'+beginTimes[0]+' '+beginTime.substring(10,19);  
    endTime=endTimes[1]+'-'+endTimes[2]+'-'+endTimes[0]+' '+endTime.substring(10,19);
    var a =(timestamp(endTime)-timestamp(beginTime))/3600/1000;
    if(a<0){
        return -1;
    }else if (a>0){  
        return 1;
    }else if (a==0){  
        return 0;
    }else{  
        return -2  
    }  
}
//返回给定范围内的随机数
function getRandomArbitrary(min, max) {
  return parseInt(Math.random()*(max - min)+min);
}
(function($) {
	$.fn.progress = function(options) {
		var defaultVal = { 
			// 存放结束时间
			eAttr : 'data-etime',
			sAttr : 'data-stime', // 存放开始时间
			stpl : '%H%:%M%:%S%', // 还有...开始
			wTime : 500, // 以500毫秒为单位进行演算
			cTime : new Date().getTime(),
			callback: null
		};
		var s = $.extend(defaultVal, options);
		window.progressTimeInterval = 0;
		var vthis = $(this);
		var width = $(window).width();
		var runTime = function() {
			s.cTime += s.wTime;
			vthis.each(function() {
				var nthis = $(this);
				var sorgT = parseInt(nthis.attr(s.sAttr));
				var eorgT = parseInt(nthis.attr(s.eAttr));
				var porgT = parseInt(nthis.attr(s.pAttr));
				var sT = isNaN(sorgT) ? 0 : sorgT - s.cTime;
				var eT = isNaN(eorgT) ? 0 : eorgT - s.cTime;
				var showTime = function(rT, showTpl) {
					var s_ = Math.round((rT % 60000) / s.wTime);
					s_ = dateNum(Math.min(Math.floor(s_ / 1000 * s.wTime), 59));
					var m_ = dateNum(Math.floor((rT % 3600000) / 60000));
					var h_ = dateNum(Math.floor((rT % 86400000) / 3600000));
					var d_ = dateNum(Math.floor(rT / 86400000));
					nthis.attr('data-timestr', showTpl.replace(/%S%/, s_).replace(/%M%/, m_).replace(/%H%/, h_).replace(/%D%/, d_));
				};
				
				var state = 0;
				if (sT > 0) {// 即将开始
					state = 1;
					showTime(sT, s.stpl);
				} else if (eT > 0) {//正在进行
					state = 2;
				} else {// 比赛结束
					state = 3;
				}
				s.callback && s.callback(state);
			});
		};
		
		runTime();
		window.progressTimeInterval = setInterval(function() {
			runTime();
		}, s.wTime);
	};
	
	$.fn.countDown = function(options) {
		var defaultVal = {
			// 存放结束时间
			eAttr : 'etime',
			sAttr : 'stime', // 存放开始时间
			wTime : 100, // 以100毫秒为单位进行演算
			etpl : '%H%:%M%:%S%', // 还有...结束
			stpl : '%H%:%M%:%S%', // 还有...开始
			sdtpl : '已开始',
			otpl : '活动已结束', // 过期显示的文本模版
			stCallback: null,
			sdCallback: null,
			otCallback: null
		};
		var dateNum = function(num) {
			return num < 10 ? '0' + num : num;
		};
		var subNum = function(num){
			numF = num.toString().substring(0,1);
			numS = num.toString().substring(1,num.length);
			return num = "<label>"+ numF + "</label><label>" + numS + '</label>';
		};
		var s = $.extend(defaultVal, options);
		var vthis = $(this);
		var runTime = function() {
			var nowTime = new Date().getTime();
			vthis.each(function() {
				var nthis = $(this);
				var sorgT = parseInt(nthis.attr(s.sAttr)) * 1000;
				var eorgT = parseInt(nthis.attr(s.eAttr)) * 1000;
				var sT = isNaN(sorgT) ? 0 : sorgT - nowTime;
				var eT = isNaN(eorgT) ? 0 : eorgT - nowTime;
				var showTime = function(rT, showTpl) {
					var s_ = Math.round((rT % 60000) / s.wTime);
					s_ = subNum(dateNum(Math.round(s_ / 1000 * s.wTime)));
					var m_ = subNum(dateNum(Math.floor((rT % 3600000) / 60000)));
					var h_ = subNum(dateNum(Math.floor((rT % 86400000) / 3600000)));
					var d_ = subNum(dateNum(Math.floor(rT / 86400000)));
					nthis.html(showTpl.replace(/%S%/, s_).replace(/%M%/, m_).replace(/%H%/, h_).replace(/%D%/, d_));
				};
				if (sT > 0) {
					showTime(sT, s.stpl);
					s.stCallback && s.stCallback();
				} else if (eT > 0) {
					showTime(eT, s.etpl);
					s.sdCallback && s.sdCallback();
				} else {
					nthis.html(s.otpl);
					s.otCallback && s.otCallback();
				}

			});
		};

		setInterval(function() {
			runTime();
		}, s.wTime);
	};
	
})(Zepto);

//删除参数值
function replaceParamVal(href,paramName,replaceWith) {
    var re=eval('/('+ paramName+'=)([^&]*)/gi');
    var nUrl = href.replace(re,paramName+'='+replaceWith);
    return nUrl;
}

function delQueStr(url, ref) //删除参数值
{
    var str = "";

    if (url.indexOf('?') != -1)
        str = url.substr(url.indexOf('?') + 1);
    else
        return url;
    var arr = "";
    var returnurl = "";
    var setparam = "";
    if (str.indexOf('&') != -1) {
        arr = str.split('&');
        for (i in arr) {
            if (arr[i].split('=')[0] != ref) {
                returnurl = returnurl + arr[i].split('=')[0] + "=" + arr[i].split('=')[1] + "&";
            }
        }
        return url.substr(0, url.indexOf('?')) + "?" + returnurl.substr(0, returnurl.length - 1);
    }
    else {
        arr = str.split('=');
        if (arr[0] == ref)
            return url.substr(0, url.indexOf('?'));
        else
            return url;
    }
}

var add_yao_prefix = function(url) {
	return 'http://yao.qq.com/tv/entry?redirect_uri=' + encodeURIComponent(url);
};

var is_android = function() {
	var ua = navigator.userAgent.toLowerCase();
	return ua.indexOf("android") > -1;
};

var getUrl = function(openid) {
	var href = window.location.href;
	href = add_param(share_url.replace(/[^\/]*\.html/i, 'index.html'), 'resopenid', hex_md5(openid), true);
	href = add_param(href, 'froms', 'share', true);
	href = delQueStr(href, "openid");
	href = delQueStr(href, "headimgurl");
	href = delQueStr(href, "nickname");
	return add_yao_prefix(href);
};
var is_undefined_null = function(data){
	
	data.ad = DataNum (data.ad);
	data.ph = DataNum (data.ph);
	data.rn =data.rn?data.rn:'';
	data.rn =data.rn!='undefined'?data.rn:'';
	function DataNum (Num){
		Num = Num?Num:'';
		Num = Num=="undefined"?'':Num;
		return Num;
	}
	
	return data;

};

(function($) {
	$.fn.progress = function(options) {
		var defaultVal = { 
			// 存放结束时间
			eAttr : 'data-etime',
			sAttr : 'data-stime', // 存放开始时间
			stpl : '%H%:%M%:%S%', // 还有...开始
			wTime : 500, // 以500毫秒为单位进行演算
			cTime : new Date().getTime(),
			callback: null
		};
		var s = $.extend(defaultVal, options);
		window.progressTimeInterval = 0;
		var vthis = $(this);
		var width = $(window).width();
		var runTime = function() {
			s.cTime += s.wTime;
			vthis.each(function() {
				var nthis = $(this);
				var sorgT = parseInt(nthis.attr(s.sAttr));
				var eorgT = parseInt(nthis.attr(s.eAttr));
				var porgT = parseInt(nthis.attr(s.pAttr));
				var sT = isNaN(sorgT) ? 0 : sorgT - s.cTime;
				var eT = isNaN(eorgT) ? 0 : eorgT - s.cTime;
				var showTime = function(rT, showTpl) {
					var s_ = Math.round((rT % 60000) / s.wTime);
					s_ = dateNum(Math.min(Math.floor(s_ / 1000 * s.wTime), 59));
					var m_ = dateNum(Math.floor((rT % 3600000) / 60000));
					var h_ = dateNum(Math.floor((rT % 86400000) / 3600000));
					var d_ = dateNum(Math.floor(rT / 86400000));
					nthis.attr('data-timestr', showTpl.replace(/%S%/, s_).replace(/%M%/, m_).replace(/%H%/, h_).replace(/%D%/, d_));
				};
				
				var state = 0;
				if (sT > 0) {// 即将开始
					state = 1;
					showTime(sT, s.stpl);
				} else if (eT > 0) {//正在进行
					state = 2;
				} else {// 比赛结束
					state = 3;
				}
				s.callback && s.callback(state);
			});
		};
		
		runTime();
		window.progressTimeInterval = setInterval(function() {
			runTime();
		}, s.wTime);
	};
})(Zepto);

$(function() {
//	var $copyright = $('.copyright');
//	if($copyright){
//			$copyright.html(copyright);
//	};
//	var cbUrl = window.location.href;
//	if(cbUrl.indexOf('cb41faa22e731e9b') < 0 ){
//		$('#div_subscribe_area').css('height', '0');
//	} else {
//		$('#div_subscribe_area').css('height', '50px');
//	};
//	$("script").each(function(i, item) {
//		var scr = $(this).attr("src");
//		$(this).attr("src", scr + "?v=" + version);
//	});
//	$("link").each(function(i, item) {
//		var href = $(this).attr("href");
//		// $(this).attr("href", href + "?v=" + version);
//	});
//	
//	$.ajax({
//		type : "get",
//		async : false,
//		url : domain_url + "api/common/versioncheck",
//		dataType : "jsonp",
//		jsonp : "callback",
//		jsonpCallback : "commonApiVersionHandler",
//		success : function(data) {
//			if (!data.result){
//				location.href = data.redirect;
//			}
//			share_img = data.si;
//			share_title = data.st;
//			share_desc = data.sd;
//			share_group = data.sgt;
//			// 一键分享
//			window['shaketv'] && shaketv.wxShare(share_img, share_title, share_desc, getUrl(openid));
//			new Authorize({callBackPage:"index.html"}).init(check_weixin_login());
//			var typeofAppid = typeof(follow_shaketv_appid);
//			if (typeofAppid == 'undefined' || typeofAppid == '' || typeofAppid == null) {
//				return;
//			} else {
//				if(openid && $("body").attr("shaketv-apid")){
//					window['shaketv'] && shaketv.subscribe($("body").attr("shaketv-apid"), function (returnData) {
//					});
//				};
//			};
//		},
//		error : function() {
//			new Authorize({callBackPage:"index.html"}).init(check_weixin_login());
//		}
//	});
//	
//	
//	// 从data_collect.js里转移过来的
//	recordUserPage(openid, $('title').html(), "");
//	$('body').delegate("*[data-collect='true']", "click", function(e) {
//		e.preventDefault();
//		
//		if ($(this).attr('data-stoppropagation') == 'true') {
//			e.stopPropagation();
//		}
//		recordUserOperate(openid, $(this).attr("data-collect-desc"), $(this).attr("data-collect-flag"));
//		
//		if($(this).attr("data-cookie") && $(this).attr("data-cookie-time")){
//			var ckData = $(this).attr("data-cookie-time")/10;
//			$.fn.cookie(H.lottery.przDateStr+'-'+openid+'-'+$(this).attr("data-cookie"),true,{expires:ckData});
//		}
//		
//		var href = $(this).attr('href'); 
//		if (href && href !== '#') {
//			if (gefrom) {
//				href = add_param(href, 'gefrom', gefrom, true);
//			}
//			setTimeout(function() {
//				window.location.href = href;
//			}, 5);
//		}
//	});
});