/**
 * Created by python on 19-12-11.
 */

$(document).ready(function () {
    toastr.options.positionClass = 'toast-center-center';
});

// 点击评论显示评论内容
function comment(id) {
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
        data: JSON.stringify(id),
        // result 为请求的返回结果对象
        success: function (result) {
            if (result.code == '1') {
                // $('#'+id).attr('style', 'display:none');
                var content = '';
                content += '<div id="div_' + id +'" style="background-color: #5cebff">';
                for(i=0;i<result.data.length;i++){
                    content += '<h5>'+result.data[i]['username'] + ':' +result.data[i]['comment'] +'</h5>';
                }
                content += '<input id="text'+ id + '" class="form-control" style="width: 400px;" onchange="change_input('+id+')" placeholder="写下你的评论...">';
                // content += '<button class="btn btn-danger" onclick="hide('+id+')">收起评论</button>';
                content += '<button class="btn btn-warning" onclick="send('+id+')" disabled id="send' + id + '">发送</button>';
                content += '</div>';
                $('#th_'+id).append(content);
                var button_text = $('#'+id).text();
                $('#'+id).text('收起评论');
                $('#'+id).attr("onclick","hide('" + id + "','" +  button_text + "')");
            } else {

            }
        }
    });
}

//　点击收回评论，删除评论内容，显示原来按钮
function hide(id, button_list) {
    $('#div_'+id).remove();
    // $('#'+id).removeAttr('style');
    $('#'+id).text(button_list);
    $('#'+id).attr("onclick","comment(this.id);");
}

// 点击发送框时删除里面的文字
function change_input(id) {
    var text_value = $("#text" + id).val();
    console.log(text_value.length);
    if (text_value.length > 0){
        $("#send" + id).removeAttr('disabled');
    }else{
        $("#send" + id).attr('disabled', true);
    }
}

//　发送用户写的评论
function send(id) {
    var text = $('#text' + id).val();
    data_dict = {
        "id":id,
        "text":text
    };
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