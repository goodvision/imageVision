var login_btn = document.getElementById("login_btn"),
logout_btn = document.getElementById("logout_btn");
function login(){
T.login(function(loginStatus){
getUserInfo();
login_btn.style.display = "none"
logout_btn.style.display = "inline-block";
},function(loginError){
alert(loginError.message);
});
}
function logout(){
logout_btn.style.display = "none";
login_btn.style.display = "inline-block";
T.logout();
var expires = new Date(); 
expires.setTime(expires.getTime()-1);//将expires设为一个过去的日期，浏览器会自动删除它
document.cookie = 'loginUser'+"=; expires="+expires.toGMTString(); 
}
function getUserInfo(){
T.api("/user/info")
.success(function(response){
if(response.ret === 0){
var html="",data=response.data;
imgsrc = data.head+"/30";
document.getElementById('nick').value = data.nick;
document.getElementById('openid').value = data.openid;
document.getElementById('head').value = data.head+"/40";;
html = '<a class="head_img" href="http://t.qq.com/'+ data.name +'" target="_blank"><img src="'+ imgsrc +'" style="margin-bottom:5px;"/></a><span class="logout_right"><a class="nick_text" href="http://t.qq.com/' + data.name +'" target="_blank" title="'+data.nick +'">'+ data.nick +'</a><a class="logout_text" id="logout_text"　href="javascript:void(0);">退出</a></span>';
logout_btn.innerHTML = html;
var logout_text = document.getElementById("logout_text");
logout_text.onclick = logout;
document.cookie="loginUser="+data.nick;
}else{
              alert(response.ret);
}
})
.error(function(code,message){
alert(message);
});
}
function init(){
T.init({appkey:801513636});
if(!T.loginStatus()){
login_btn.style.display = "inline-block";
logout_btn.style.display = "none";
}else{
getUserInfo();
login_btn.style.display = "none";
logout_btn.style.display = "inline-block";
}
login_btn.onclick = login;
}
init();
