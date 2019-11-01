/**
 * Created by python on 19-10-30.
 */
function registerData() {
    var username = $('#username').val();
    var password = $('#password').val();
    var mobile = $('#mobile').val();
    var registerdata = {
        "username": username,
        "password": password,
        "mobile": mobile
    };
    $.post('/register/',
        registerdata, function (data) {
            if (data != '500') {
                alert('注册成功');
                window.location.href = '/login';
            }
            else {
                alert('注册失败');
            }
        });
}

function loginData() {
    var username = $('#username').val();
    var password = $('#password').val();
    var logindata = {
        "username": username,
        "password": password
    };
    $.post('/login/',
        logindata, function (data) {
            if (data != '500') {
                alert('登陆成功');
                window.location.href = '/index';
            }
            else {
                alert('登陆失败，账号密码不正确');
            }

        });
}

function imageData(id) {
    image_id = {"id":id};
    $.post('/user/',
        image_id, function (data) {
        var imagedata = JSON.parse(data);
            if (data != '500'){
                $('#imageid').html('');
                $('#imageid').append("<img src=" + imagedata.images + " width='200px'>"+
            "<h1>" + imagedata.content_one + "</h1>"+
            "<h2>"+imagedata.content_two+"</h2>")
            }else{

            }


        });
}