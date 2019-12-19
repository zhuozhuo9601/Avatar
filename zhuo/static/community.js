/**
 * Created by python on 19-12-11.
 */

$(document).ready(function () {
    toastr.options.positionClass = 'toast-center-center';
});

// 点击评论显示评论内容
function comment(id, page) {
    com_dict = {};
    if (!page) {
        page = 1;
        com_dict['status'] = 'no'
    } else {
        com_dict['status'] = 'yes'
    }
    com_dict["page"] = page;
    com_dict["id"] = id;
    $.ajax({
        // 请求方式
        type: "post",
        // contentType
        contentType: "application/json",
        // dataType
        dataType: "json",
        // url
        url: /comment/,
        // 把JS的对象或数组序列化一个json 字符串
        data: JSON.stringify(com_dict),
        // result 为请求的返回结果对象
        success: function (result) {
            if (result.code == '1') {
                var button_text = $('#' + id).text();
                // $('#'+id).attr('style', 'display:none');
                var content = '';
                var page_content = '';
                if (result.status == 'no') {
                    $('#' + id).text('收起评论');
                    $('#' + id).attr("onclick", "hide('" + id + "','" + button_text + "')");
                } else {
                    // for (i = 0; i < result.data.length; i++) {
                    //     $("#h_" + id + "_" + i).text(result.data[i]['username'] + ':' + result.data[i]['comment']);
                    // }
                    $('#page' + id).remove();
                    $('#div_' + id).remove();
                }
                content += '<div id="div_' + id + '" style="background-color: #d5ffd1;border: 1px;border-style: dotted;">';
                for (i = 0; i < result.data.length; i++) {
                    content += '<h5 id="h_' + id + "_" + i + '">' + result.data[i]['username'] + ':' + result.data[i]['comment'] + '</h5>';
                }
                content += '<input id="text' + id + '" class="form-control" style="width: 400px;" onchange="change_input(' + id + ')" placeholder="写下你的评论...">';
                // content += '<button class="btn btn-danger" onclick="hide('+id+')">收起评论</button>';
                content += '<button class="btn btn-warning" onclick="send(' + id + ')" disabled id="send' + id + '">发送</button>';
                content += '</div>';
                page_content += '<div id="page' + id + '">';
                page_content += '<ul class="pagination" id="pager">';
                // {#上一页按钮开始#}
                // {# 如果当前页有上一页#}
                if (result.has_previous != '0') {
                    page_content += '<li><a onclick="comment(' + id + "," + result.has_previous + ')">上一页</a></li>';
                }
                // {#  当前页的上一页按钮正常使用#}
                else {
                    page_content += '<li class="previous disabled" disabled><a href="#">上一页</a></li>';
                }
                // {# 当前页的不存在上一页时,上一页的按钮不可用#}
                // {#上一页按钮结束#}
                // {# 页码开始#}
                for (i = 0; i < result.page_list.length; i++) {
                    if (page == result.page_list[i]){
                        page_content += '<li><a style="color: #ff0009;" onclick="comment(' + id + "," + result.page_list[i] + ')">' + result.page_list[i] + '</a></li>';
                    }else{
                        page_content += '<li><a onclick="comment(' + id + "," + result.page_list[i] + ')">' + result.page_list[i] + '</a></li>';
                    }

                }
                // {#页码结束#}
                // {# 下一页按钮开始#}
                if (result.has_next != '0') {
                    page_content += '<li><a onclick="comment(' + id + "," + result.has_next + ')">下一页</a></li>';
                }
                else {
                    page_content += '<li class="next disabled"><a href="#">下一页</a></li>';
                }
                // {# 下一页按钮结束#}
                page_content += '</ul>';
                page_content += '</div>';
                $('#th_' + id).append(content);
                $('#th_' + id).append(page_content);

            } else {

            }
        }
    });
}

//　点击收回评论，删除评论内容，显示原来按钮
function hide(id, button_list) {
    $('#div_' + id).remove();
    $('#page' + id).remove();
    // $('#'+id).removeAttr('style');
    $('#' + id).text(button_list);
    $('#' + id).attr("onclick", "comment(this.id);");
}

// 点击发送框时删除里面的文字
function change_input(id) {
    var text_value = $("#text" + id).val();
    if (text_value.length > 0) {
        $("#send" + id).removeAttr('disabled');
    } else {
        $("#send" + id).attr('disabled', true);
    }
}

//　发送用户写的评论
function send(id) {
    var text = $('#text' + id).val();
    data_dict = {
        "id": id,
        "text": text
    };
    $('#text' + id).val('');
    $("#send" + id).attr('disabled', 'disabled');
    $.ajax({
        // 请求方式
        type: "post",
        // contentType
        contentType: "application/json",
        // dataType
        dataType: "json",
        // url
        url: /comm_store/,
        // 把JS的对象或数组序列化一个json 字符串
        data: JSON.stringify(data_dict),
        // result 为请求的返回结果对象
        success: function (result) {
            if (result.code == '1') {
                toastr.success(result.msg);
            } else {
                toastr.error(result.msg);
            }
        }
    });
}

// 用户点赞
function like_method(id) {
    com_id = id.split('like')[1];
    $.ajax({
        // 请求方式
        type: "post",
        // contentType
        contentType: "application/json",
        // dataType
        dataType: "json",
        // url
        url: /comm_like/,
        // 把JS的对象或数组序列化一个json 字符串
        data: JSON.stringify(com_id),
        // result 为请求的返回结果对象
        success: function (result) {
            if (result.code == '1') {
                $("#"+id).text(result.like);

            } else {
                toastr.error(result.like);
            }
        }
    });
}