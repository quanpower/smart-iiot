webpackJsonp([29],{1229:function(e,t,n){"use strict";function a(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var u=n(118),s=a(u),r=(n(292),n(1266)),o=a(r),i=n(1290),c=n(2804),f=n(121),l=a(f);t.default=(0,o.default)(i.model,{namespace:"tianshuoOnOff",state:{switch:[]},subscriptions:{setup:function(e){e.dispatch;e.history.listen(function(e){var t=e.pathname;(0,l.default)("/tianshuo_on_off").exec(t)?console.log("switch tianshuo on/off begin---"):console.log("we are at:",t)})}},effects:{updateTianshuoOnOff:s.default.mark(function e(t,n){var a,u=t.payload,r=n.call;n.put;return s.default.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return console.log("payload",u),e.next=3,r(c.switchTianshuoOnOff,u);case 3:if(a=e.sent,!a.success){e.next=8;break}console.log(a),e.next=9;break;case 8:throw a;case 9:case"end":return e.stop()}},e,this)})}}),e.exports=t.default},1266:function(e,t,n){"use strict";function a(e){return e&&e.__esModule?e:{default:e}}function u(){for(var e={state:{},subscriptions:{},effects:{},reducers:{}},t=arguments.length,n=Array(t),a=0;a<t;a++)n[a]=arguments[a];return n.reduce(function(e,t){return e.namespace=t.namespace,"object"!==(0,i.default)(t.state)||Array.isArray(t.state)?"state"in t&&(e.state=t.state):(0,r.default)(e.state,t.state),(0,r.default)(e.subscriptions,t.subscriptions),(0,r.default)(e.effects,t.effects),(0,r.default)(e.reducers,t.reducers),e},e)}Object.defineProperty(t,"__esModule",{value:!0});var s=n(290),r=a(s),o=n(64),i=a(o);t.default=u},1290:function(e,t,n){"use strict";function a(e){return e&&e.__esModule?e:{default:e}}var u=n(3),s=a(u),r=n(1266),o=a(r),i={reducers:{updateState:function(e,t){var n=t.payload;return(0,s.default)({},e,n)}}},c=(0,o.default)(i,{state:{list:[],pagination:{showSizeChanger:!0,showQuickJumper:!0,showTotal:function(e){return"Total "+e+" Items"},current:1,total:0}},reducers:{querySuccess:function(e,t){var n=t.payload,a=n.list,u=n.pagination;return(0,s.default)({},e,{list:a,pagination:(0,s.default)({},e.pagination,u)})}}});e.exports={model:i,pageModel:c}},2804:function(e,t,n){"use strict";function a(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0}),t.switchTianshuoOnOff=void 0;var u=n(118),s=a(u),r=n(287),o=a(r),i=(t.switchTianshuoOnOff=function(){var e=(0,o.default)(s.default.mark(function e(t){return s.default.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",(0,i.request)({url:f,method:"post",data:t}));case 1:case"end":return e.stop()}},e,this)}));return function(t){return e.apply(this,arguments)}}(),n(75)),c=i.config.api,f=c.tianshuoOnOffControl}});