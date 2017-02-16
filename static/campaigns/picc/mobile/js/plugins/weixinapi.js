/**!
 * 微信内置浏览器的Javascript API，功能包括：
 *
 * 1、分享到微信朋友圈
 * 2、分享给微信好友
 * 3、分享到腾讯微博
 * 4、新的分享接口，包含朋友圈、好友、微博的分享（for iOS）
 * 5、隐藏/显示右上角的菜单入口
 * 6、隐藏/显示底部浏览器工具栏
 * 7、获取当前的网络状态
 * 8、调起微信客户端的图片播放组件
 * 9、关闭公众平台Web页面
 * 10、判断当前网页是否在微信内置浏览器中打开
 * 11、增加打开扫描二维码
 * 12、支持WeixinApi的错误监控
 * 13、检测应用程序是否已经安装（需要官方开通权限）
 * 14、发送电子邮件
 *
 * @author zhaoxianlie(http://www.baidufe.com)
 */
(function (window) {

    "use strict";

    /**
     * 定义WeixinApi
     */
    var WeixinApi = {
        version: 3.5
    };

    // 将WeixinApi暴露到window下：全局可使用，对旧版本向下兼容
    window.WeixinApi = WeixinApi;

    /////////////////////////// CommonJS /////////////////////////////////
    if (typeof define === 'function' && (define.amd || define.cmd)) {
        if (define.amd) {
            // AMD 规范，for：requirejs
            define(function () {
                return WeixinApi;
            });
        } else if (define.cmd) {
            // CMD 规范，for：seajs
            define(function (require, exports, module) {
                module.exports = WeixinApi;
            });
        }
    }

    /**
     * 对象简单继承，后面的覆盖前面的，继承深度：deep=1
     * @private
     */
    var _extend = function () {
        var result = {}, obj, k;
        for (var i = 0, len = arguments.length; i < len; i++) {
            obj = arguments[i];
            if (typeof obj === 'object') {
                for (k in obj) {
                    obj[k] && (result[k] = obj[k]);
                }
            }
        }
        return result;
    };

    /**
     * 内部私有方法，分享用
     * @private
     */
    var _share = function (cmd, data, callbacks) {
        callbacks = callbacks || {};

        // 分享过程中的一些回调
        var progress = function (resp) {
            switch (true) {
                // 用户取消
                case /\:cancel$/i.test(resp.err_msg) :
                    callbacks.cancel && callbacks.cancel(resp);
                    break;
                // 发送成功
                case /\:(confirm|ok)$/i.test(resp.err_msg):
                    callbacks.confirm && callbacks.confirm(resp);
                    break;
                // fail　发送失败
                case /\:fail$/i.test(resp.err_msg) :
                default:
                    callbacks.fail && callbacks.fail(resp);
                    break;
            }
            // 无论成功失败都会执行的回调
            callbacks.all && callbacks.all(resp);
        };

        // 执行分享，并处理结果
        var handler = function (theData, argv) {

            // 据用户反馈，貌似Android上的分享到朋友圈是OK的，iOS不太对
            if (cmd.menu == 'menu:share:timeline' ||
                (cmd.menu == 'menu:general:share' && argv.shareTo == 'timeline')) {

                // 判断是否为Android
                var isAndroid = /android/i.test(navigator.userAgent);
                if (!isAndroid) {
                    var title = theData.title;
                    theData.title = theData.desc || title;
                    theData.desc = title || theData.desc;
                }
            }

            // 新的分享接口，单独处理
            if (cmd.menu === 'menu:general:share') {
                // 如果是收藏操作，并且在wxCallbacks中配置了favorite为false，则不执行回调
                if (argv.shareTo == 'favorite' || argv.scene == 'favorite') {
                    if (callbacks.favorite === false) {
                        return argv.generalShare(theData, function () {
                        });
                    }
                }

                argv.generalShare(theData, progress);
            } else {
                WeixinJSBridge.invoke(cmd.action, theData, progress);
            }
        };

        // 监听分享操作
        WeixinJSBridge.on(cmd.menu, function (argv) {
            callbacks.dataLoaded = callbacks.dataLoaded || new Function();
            if (callbacks.async && callbacks.ready) {
                WeixinApi["_wx_loadedCb_"] = callbacks.dataLoaded;
                if (WeixinApi["_wx_loadedCb_"].toString().indexOf("_wx_loadedCb_") > 0) {
                    WeixinApi["_wx_loadedCb_"] = new Function();
                }
                callbacks.dataLoaded = function (newData) {
                    callbacks.__cbkCalled = true;
                    var theData = _extend(data, newData);
                    theData.img_url = theData.imgUrl || theData.img_url;
                    delete theData.imgUrl;
                    WeixinApi["_wx_loadedCb_"](theData);
                    handler(theData, argv);
                };
                // 然后就绪
                if (!(argv && (argv.shareTo == 'favorite' || argv.scene == 'favorite') && callbacks.favorite === false)) {
                    callbacks.ready && callbacks.ready(argv, data);
                    // 如果设置了async为true，但是在ready方法中并没有手动调用dataLoaded方法，则自动触发一次
                    if (!callbacks.__cbkCalled) {
                        callbacks.dataLoaded({});
                        callbacks.__cbkCalled = false;
                    }
                }
            } else {
                // 就绪状态
                var theData = _extend(data);
                if (!(argv && (argv.shareTo == 'favorite' || argv.scene == 'favorite') && callbacks.favorite === false)) {
                    callbacks.ready && callbacks.ready(argv, theData);
                }
                handler(theData, argv);
            }
        });
    };

    /**
     * 分享到微信朋友圈
     * @param       {Object}    data       待分享的信息
     * @p-config    {String}    appId      公众平台的appId（服务号可用）
     * @p-config    {String}    imgUrl     图片地址
     * @p-config    {String}    link       链接地址
     * @p-config    {String}    desc       描述
     * @p-config    {String}    title      分享的标题
     *
     * @param       {Object}    callbacks  相关回调方法
     * @p-config    {Boolean}   async                   ready方法是否需要异步执行，默认false
     * @p-config    {Function}  ready(argv, data)       就绪状态
     * @p-config    {Function}  dataLoaded(data)        数据加载完成后调用，async为true时有用，也可以为空
     * @p-config    {Function}  cancel(resp)    取消
     * @p-config    {Function}  fail(resp)      失败
     * @p-config    {Function}  confirm(resp)   成功
     * @p-config    {Function}  all(resp)       无论成功失败都会执行的回调
     */
    WeixinApi.shareToTimeline = function (data, callbacks) {
        _share({
            menu: 'menu:share:timeline',
            action: 'shareTimeline'
        }, {
            "appid": data.appId ? data.appId : '',
            "img_url": data.imgUrl,
            "link": data.link,
            "desc": data.desc,
            "title": data.title,
            "img_width": "640",
            "img_height": "640"
        }, callbacks);
    };

    /**
     * 发送给微信上的好友
     * @param       {Object}    data       待分享的信息
     * @p-config    {String}    appId      公众平台的appId（服务号可用）
     * @p-config    {String}    imgUrl     图片地址
     * @p-config    {String}    link       链接地址
     * @p-config    {String}    desc       描述
     * @p-config    {String}    title      分享的标题
     *
     * @param       {Object}    callbacks  相关回调方法
     * @p-config    {Boolean}   async                   ready方法是否需要异步执行，默认false
     * @p-config    {Function}  ready(argv, data)       就绪状态
     * @p-config    {Function}  dataLoaded(data)        数据加载完成后调用，async为true时有用，也可以为空
     * @p-config    {Function}  cancel(resp)    取消
     * @p-config    {Function}  fail(resp)      失败
     * @p-config    {Function}  confirm(resp)   成功
     * @p-config    {Function}  all(resp)       无论成功失败都会执行的回调
     */
    WeixinApi.shareToFriend = function (data, callbacks) {
        _share({
            menu: 'menu:share:appmessage',
            action: 'sendAppMessage'
        }, {
            "appid": data.appId ? data.appId : '',
            "img_url": data.imgUrl,
            "link": data.link,
            "desc": data.desc,
            "title": data.title,
            "img_width": "640",
            "img_height": "640"
        }, callbacks);
    };

    /**
     * 新的分享接口
     * @param       {Object}    data       待分享的信息
     * @p-config    {String}    appId      公众平台的appId（服务号可用）
     * @p-config    {String}    imgUrl     图片地址
     * @p-config    {String}    link       链接地址
     * @p-config    {String}    desc       描述
     * @p-config    {String}    title      分享的标题
     *
     * @param       {Object}    callbacks  相关回调方法
     * @p-config    {Boolean}   async                   ready方法是否需要异步执行，默认false
     * @p-config    {Function}  ready(argv, data)       就绪状态
     * @p-config    {Function}  dataLoaded(data)        数据加载完成后调用，async为true时有用，也可以为空
     * @p-config    {Function}  cancel(resp)    取消
     * @p-config    {Function}  fail(resp)      失败
     * @p-config    {Function}  confirm(resp)   成功
     * @p-config    {Function}  all(resp)       无论成功失败都会执行的回调
     */
    WeixinApi.generalShare = function (data, callbacks) {
        _share({
            menu: 'menu:general:share'
        }, {
            "appid": data.appId ? data.appId : '',
            "img_url": data.imgUrl,
            "link": data.link,
            "desc": data.desc,
            "title": data.title,
            "img_width": "640",
            "img_height": "640"
        }, callbacks);
    };

    /**
     * 显示网页右上角的按钮
     */
    WeixinApi.showOptionMenu = function () {
        WeixinJSBridge.call('showOptionMenu');
    };


    /**
     * 隐藏网页右上角的按钮
     */
    WeixinApi.hideOptionMenu = function () {
        WeixinJSBridge.call('hideOptionMenu');
    };

    /**
     * 显示底部工具栏
     */
    WeixinApi.showToolbar = function () {
        WeixinJSBridge.call('showToolbar');
    };

    /**
     * 隐藏底部工具栏
     */
    WeixinApi.hideToolbar = function () {
        WeixinJSBridge.call('hideToolbar');
    };

    /**
     * 当页面加载完毕后执行，使用方法：
     * WeixinApi.ready(function(Api){
     *     // 从这里只用Api即是WeixinApi
     * });
     * @param readyCallback
     */
    WeixinApi.ready = function (readyCallback) {
        if (readyCallback && typeof readyCallback == 'function') {
            var Api = this;
            var wxReadyFunc = function () {
                readyCallback(Api);
            };
            if (typeof window.WeixinJSBridge == "undefined") {
                if (document.addEventListener) {
                    document.addEventListener('WeixinJSBridgeReady', wxReadyFunc, false);
                } else if (document.attachEvent) {
                    document.attachEvent('WeixinJSBridgeReady', wxReadyFunc);
                    document.attachEvent('onWeixinJSBridgeReady', wxReadyFunc);
                }
            } else {
                wxReadyFunc();
            }
        }
    };

    /**
     * 判断当前网页是否在微信内置浏览器中打开
     */
    WeixinApi.openInWeixin = function () {
        return /MicroMessenger/i.test(navigator.userAgent);
    };

    /**
     * 开启Api的debug模式，比如出了个什么错误，能alert告诉你，而不是一直很苦逼的在想哪儿出问题了
     * @param    {Function}  callback(error) 出错后的回调，默认是alert
     */
    WeixinApi.enableDebugMode = function (callback) {
        /**
         * @param {String}  errorMessage   错误信息
         * @param {String}  scriptURI      出错的文件
         * @param {Long}    lineNumber     出错代码的行号
         * @param {Long}    columnNumber   出错代码的列号
         */
        window.onerror = function (errorMessage, scriptURI, lineNumber, columnNumber) {

            // 有callback的情况下，将错误信息传递到options.callback中
            if (typeof callback === 'function') {
                callback({
                    message: errorMessage,
                    script: scriptURI,
                    line: lineNumber,
                    column: columnNumber
                });
            } else {
                // 其他情况，都以alert方式直接提示错误信息
                var msgs = [];
                msgs.push("额，代码有错。。。");
                msgs.push("\n错误信息：", errorMessage);
                msgs.push("\n出错文件：", scriptURI);
                msgs.push("\n出错位置：", lineNumber + '行，' + columnNumber + '列');
                alert(msgs.join(''));
            }
        }
    };

})(window);
