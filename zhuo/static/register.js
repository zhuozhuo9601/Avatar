/**
 * Created by python on 19-10-30.
 */
layui.use(['layer'], function () {
    var layer = layui.layer;//滑块

});
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
            j_data = JSON.parse(data);
            if (j_data.code != '0') {
                layer.msg(j_data.msg, {icon: 6});
                window.location.href = '/login';
            } else {
                layer.msg(j_data.msg, {icon: 5});
                window.location.href = '/register';
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
            if (data != '0') {
                layer.msg('登陆成功', {icon: 6});
                window.location.href = '/';
            }
            else {
                layer.msg('登陆失败', {icon: 5});
                window.location.href = '/login';
            }

        });
}

function imageData(id) {
    image_id = {"id": id};
    $.post('/user/',
        image_id, function (data) {
            var imagedata = JSON.parse(data);
            if (imagedata.code != '0') {
                $('#imageid').html('');
                $('#imageid').append("<img src=" + imagedata.images.images + " width='200px'>" +
                    "<h1>" + imagedata.images.content_one + "</h1>" +
                    "<h2>" + imagedata.images.content_two + "</h2>");
            } else {
                layer.msg(imagedata.msg, {icon: 5});
            }


        });
}

// 省市区三级联动
function city_Linkage() {
    alert('选中了');
    console.log('sadsadada');
}
