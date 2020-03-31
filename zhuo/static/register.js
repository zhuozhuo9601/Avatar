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

// 检查账号密码格式是否正确
function examination(id, status) {
    var reg_name = /(^[a-zA-Z][a-zA-Z0-9_]{4,15}$)/;
    var reg_word = /(^[0-9A-Za-z]{6,20}$)/;
    var reg_phone = /(^1[3-9]\d{9}$)/;
    if (status == 'name') {
        if (reg_name.test($("#" + id).val()) == false) {
            $("#username_error").removeAttr('hidden');
        }
    } else if (status == 'word') {
        if (reg_word.test($("#" + id).val()) == false) {
            $("#password_error").removeAttr('hidden');
        }
    } else {
        if (reg_phone.test($("#" + id).val()) == false) {
            $("#phone_error").removeAttr('hidden');
        }
    }
}

// 重新刷新验证码
$(function () {
    bindGetValidCode()
});
function bindGetValidCode() {
    // 点击刷新验证码
    $("#code").click(function () {
        console.log($(this).attr('src'));
        $(this)[0].src += "?"

    })
}