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
                    layer.msg(j_data.msg);
                    window.location.href = '/login';
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
                j_data = JSON.parse(data);
                if (j_data.code != '0') {
                    layer.msg('登陆成功');
                    window.location.href = '/index';
                }
                else {

                    layer.msg(j_data.msg);
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
                        "<h2>" + imagedata.images.content_two + "</h2>")
                } else {
                    layer.msg(imagedata.msg);
                }


            });
    }