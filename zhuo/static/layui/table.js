layui.config({
    version: '1572350921010' //为了更新 js 缓存，可忽略
});

$(function () {
    layui.use(['tree', 'layer'], function () {
        var tree = layui.tree,
            layer = layui.layer;
        $.post('/table_permission/'
            , function (res) {
                if (res.code == 0) {
                    var inst1 = tree.render({
                        elem: '#tree_data'  //绑定元素
                        , data: res.data
                    });
                } else {
                    layer.msg(res.msg, {time: 1000, icon: 2});
                }

            }, 'json');

    });
});


layui.use(['laydate', 'laypage', 'layer', 'table', 'carousel', 'upload', 'element', 'slider', 'jquery'], function () {
    var laydate = layui.laydate //日期
        , laypage = layui.laypage //分页
        , layer = layui.layer //弹层
        , table = layui.table //表格
        , carousel = layui.carousel //轮播
        , upload = layui.upload //上传
        , element = layui.element //元素操作
        , slider = layui.slider
        , $ = layui.$
        , form = layui.form;//滑块
    //向世界问个好
    layer.msg('你是最棒的');

    $("#formDemo").click(function () {
        var formObject = {};
        var formArray = $("#form_id").serializeArray();
        $.each(formArray, function (i, item) {
            formObject[item.name] = item.value;
        });
        var add_dict = JSON.stringify(formObject);
        $.ajax({
            url: "/table_add/",
            type: "post",
            data: {'add_dict': add_dict},
            success: function (data) {
                j_data = JSON.parse(data);
                layer.msg(j_data.msg);
                setTimeout(function () {
                    window.location.reload();
                }, 3000);

            }
        });
    });

    //监听Tab切换
    element.on('tab(demo)', function (data) {
        layer.tips('切换了 ' + data.index + '：' + this.innerHTML, this, {
            tips: 1
        });
    });

    //执行一个 table 实例
    table.render({
        elem: '#demo'
        , height: 420
        , method: 'post'
        , url: '/table/' //数据接口
        , title: '用户表'
        , page: true //开启分页
        , toolbar: 'default' //开启工具栏，此处显示默认图标，可以自定义模板，详见文档
        , totalRow: true //开启合计行
        , cols: [[ //表头
            {type: 'checkbox', fixed: 'left'}
            , {field: 'id', title: 'ID', width: 80, sort: true, fixed: 'left', totalRowText: '合计：'}
            , {field: 'username', title: '用户名', width: 180}
            , {field: 'birthday', title: '生日', width: 190, sort: true, totalRow: true}
            , {field: 'sex', title: '性别', width: 80, sort: true}
            , {field: 'province', title: '省份', width: 80, sort: true, totalRow: true}
            , {field: 'city', title: '城市', width: 150}
            , {field: 'area', title: '区', width: 200}
            , {field: 'hobby', title: '爱好', width: 100}
            , {field: 'career', title: '职业', width: 100}
            , {field: 'sign', title: '签名', width: 205, sort: true, totalRow: true}
            , {fixed: 'right', width: 165, align: 'center', toolbar: '#barDemo'}
        ]]
    });

    //监听头工具栏事件
    table.on('toolbar(TestTable)', function (obj) {
        var checkStatus = table.checkStatus(obj.config.id)
            , data = checkStatus.data; //获取选中的数据
        switch (obj.event) {
            case 'add':
                // layer.msg('添加');
                layer.open({
                        type: 1,
                        skin: 'layui-layer-rim', //加上边框
                        area: ['820px', '640px'], //宽高
                        content: $('#form_id')
                    }
                );
                break;
            case 'update':
                if (data.length === 0) {
                    layer.msg('请选择一行');
                } else if (data.length > 1) {
                    layer.msg('只能同时编辑一个');
                } else {
                    // layer.alert('编辑 [id]：'+ checkStatus.data[0].id);
                    var id = checkStatus.data[0].id;
                    layer.open({
                        type: 1,
                        skin: 'layui-layer-rim', //加上边框
                        area: ['420px', '640px'], //宽高
                        content: '<div style="margin-top: 10px;">' +
                        '<div class="layui-form-item">' +
                        '<label class="layui-form-label" style="width: 120px">昵称：</label>' +
                        '<div class="layui-input-inline">' +
                        '<input type="text" id="username" required class="layui-input" autocomplete="off" placeholder=' + checkStatus.data[0].username + '>' +
                        '</div>' +
                        '</div>' +

                        '<div class="layui-form-item">' +
                        '<label class="layui-form-label" style="width: 120px">积分：</label>' +
                        '<div class="layui-input-inline">' +
                        '<input type="text" id="experience" required class="layui-input" autocomplete="off" placeholder=' + checkStatus.data[0].experience + '>' +
                        '</div>' +
                        '</div>' +

                        '<div class="layui-form-item">' +
                        '<label class="layui-form-label" style="width: 120px">性别：</label>' +
                        '<div class="layui-input-inline">' +
                        '<input type="text" id="sex" required class="layui-input" autocomplete="off" placeholder=' + checkStatus.data[0].sex + '>' +
                        '</div>' +
                        '</div>' +

                        '<div class="layui-form-item">' +
                        '<label class="layui-form-label" style="width: 120px">评分：</label>' +
                        '<div class="layui-input-inline">' +
                        '<input type="text" id="score" required class="layui-input" autocomplete="off" placeholder=' + checkStatus.data[0].score + '>' +
                        '</div>' +
                        '</div>' +

                        '<div class="layui-form-item">' +
                        '<label class="layui-form-label" style="width: 120px">城市：</label>' +
                        '<div class="layui-input-inline">' +
                        '<input type="text" id="city" required class="layui-input" autocomplete="off" placeholder=' + checkStatus.data[0].city + '>' +
                        '</div>' +
                        '</div>' +

                        '<div class="layui-form-item">' +
                        '<label class="layui-form-label" style="width: 120px">签名：</label>' +
                        '<div class="layui-input-inline">' +
                        '<input type="text" id="sign" required class="layui-input" autocomplete="off" placeholder=' + checkStatus.data[0].sign + '>' +
                        '</div>' +
                        '</div>' +

                        '<div class="layui-form-item">' +
                        '<label class="layui-form-label" style="width: 120px">职业：</label>' +
                        '<div class="layui-input-inline">' +
                        '<input type="text" id="classify" required class="layui-input" autocomplete="off" placeholder=' + checkStatus.data[0].classify + '>' +
                        '</div>' +
                        '</div>' +

                        '<div class="layui-form-item">' +
                        '<label class="layui-form-label" style="width: 120px">财富：</label>' +
                        '<div class="layui-input-inline">' +
                        '<input type="text" id="wealth" required class="layui-input" autocomplete="off" placeholder=' + checkStatus.data[0].wealth + '>' +
                        '</div>' +
                        '</div>' +

                        '<button class="layui-btn layui-btn-warm layui-btn-radius" id="button_update" onclick=update(' + id + ') style="margin-left: 40%;">修改</button>' +
                        '</div>'
                    })
                }
                break;
            case 'delete':
                if (data.length === 0) {
                    layer.msg('请选择一行');
                } else {
                    $.ajax({
                        url: "/table_delete/",
                        type: "post",
                        data: {'id': checkStatus.data[0].id},
                        success: function (data) {
                            j_data = JSON.parse(data);
                            layer.msg(j_data.msg);
                            setTimeout(function () {
                                window.location.reload();
                            }, 3000);

                        }
                    });
                }
                break;
        }
    });

    //监听工具条
    table.on('tool(TestTable)', function (obj) { //注：tool 是工具条事件名，test 是 table 原始容器的属性 lay-filter="对应的值"
        var data = obj.data; //获得当前行数据
        var layEvent = obj.event; //获得 lay-event 对应的值（也可以是表头的 event 参数对应的值）
        var tr = obj.tr; //获得当前行 tr 的 DOM 对象（如果有的话）

        if (layEvent === 'detail') { //查看
            detail(obj);
        } else if (layEvent === 'del') { //删除
            del(obj);
        } else if (layEvent === 'edit') { //编辑
            edit(obj);
        }
    });

    function detail(obj) {
        var html = '';
        html += '<div>';
        for (var key in obj.data) {
            html += '<div class="layui-form-item">';
            html += '<label class="layui-form-label">' + key + ':</label>';
            html += '<div class="layui-input-block">';
            html += '<span style="text-align: center;line-height: 40px;">' + obj.data[key] + '</span>';
            html += '</div>';
            html += '</div>';
        }
        html += '</div>';
        layer.open({
            type: 1,
            tips: 1,
            title: '查看',
            id: 'system',
            btn: ['确认', '取消'],
            area: ['520px', '440px'], //宽高
            content: html,
            success: function (layero, index) {

            },
            yes: function (index, layero) {
                layer.close(index);
            }
        })
    }

    function del(obj) {
        layer.msg('进行删除操作', {icon: 2});
    }

    function edit(obj) {
        layer.msg('进行编辑操作', {icon: 1});
    }

});

function update(id) {
    var username = $('#username').val();
    var experience = $('#experience').val();
    var sex = $('#sex').val();
    var score = $('#score').val();
    var city = $('#city').val();
    var sign = $('#sign').val();
    var classify = $('#classify').val();
    var wealth = $('#wealth').val();
    var update_data = {
        "id": id,
        "username": username, "experience": experience,
        "sex": sex, "score": score, "city": city, "sign": sign, "classify": classify, "wealth": wealth
    };
    var update_dict = JSON.stringify(update_data);
    $.ajax({
        url: "/table_update/",
        type: "post",
        data: {'update_dict': update_dict},
        success: function (data) {
            j_data = JSON.parse(data);
            layer.msg(j_data.msg);
            setTimeout(function () {
                window.location.reload();
            }, 3000);

        }
    });
}

function add_permission() {
    layui.use(['layer', 'table', 'element', 'form'], function () {
        var layer = layui.layer //弹层
            , form = layui.form;//滑块
        $.post('/check_permission/'
            , function (res) {
                var html = '';
                if (res.code == 0) {
                    html += '<form class="layui-form" action="" id="select_form">';
                    html += '<div class="layui-inline">';
                    html += '<label class="layui-form-label">权限app:</label>';
                    html += '<div class="layui-input-inline">';
                    html += '<select name="modules" lay-filter="select_id" lay-verify="required" lay-search="" id="select_id">';
                    for (i = 0; i < res.data.length; i++) {
                        html += '<option value=' + res.data[i] + '>' + res.data[i] + '</option>';
                    }
                    html += '</select>';
                    html += '</div>';
                    html += '</div>';
                    html += '<div class="layui-inline" id="type_id">';
                    html += '</div>';
                    html += '<div class="layui-inline" id="input_id">';
                    html += '</div>';
                    html += '</form>';

                } else {
                    layer.msg(res.msg, {time: 1000, icon: 2});
                }

                layer.open({
                    type: 1,
                    title: '添加权限',
                    id: 'system',
                    btn: ['确认', '取消'],
                    area: ['520px', '440px'], //宽高
                    content: html,
                    success: function (layero, index) {
                        form.render('select');
                    },
                    yes: function (index, layero) {
                        var select_id = $("#select_id").val();
                        var select_type = $("#select_type").val();
                        var name = $("input[name='name']").val();
                        var codename = $("input[name='codename']").val();
                        $.post('/add_permission/'
                            , {
                                'select_id': select_id,
                                'select_type': select_type,
                                'name': name,
                                'codename': codename
                            }, function (res) {
                                if (res.code == 0) {
                                    layer.msg(res.msg, {time: 1000, icon: 1});
                                } else {
                                    layer.msg(res.msg, {time: 1000, icon: 2});
                                }
                            }, 'json');
                        layer.close(index);

                    }
                })

            }, 'json');


        form.on('select(select_id)', function (data) {
            $.post('/check_permission/'
                , {'select': data.value}, function (res) {
                    var html = '';
                    if (res.code == 0) {
                        $("#type_id").html('');
                        html += '<label class="layui-form-label">权限app:</label>';
                        html += '<div class="layui-input-inline">';
                        html += '<select name="select_type" lay-filter="select_type" lay-verify="required" lay-search="" id="select_type">';
                        for (i = 0; i < res.data.length; i++) {
                            html += '<option value=' + res.data[i].id + '>' + res.data[i].model + '</option>';
                        }
                        html += '</select>';
                        html += '</div>';

                        $("#type_id").append(html);
                        form.render('select');
                    }
                }, 'json')
        });

        form.on('select(select_type)', function (data) {
            var html = '';
            html += '<label class="layui-form-label">name:</label>';
            html += '<div class="layui-input-block">';
            html += '<input type="text" name="name" required  lay-verify="required" placeholder="请输入name" autocomplete="off" class="layui-input">';
            html += '</div>';
            html += '<label class="layui-form-label">codename:</label>';
            html += '<div class="layui-input-block">';
            html += '<input type="text" name="codename" required  lay-verify="required" placeholder="请输入codename" autocomplete="off" class="layui-input">';
            html += '</div>';
            $("#input_id").append(html);
            form.render();
        });
    })
}
