/**
 * Created by python on 20-4-13.
 */
layui.use(['layer'], function () {
    var layer = layui.layer;//滑块

});
var data_result = '';
function reptile_data() {
    $.post('/reptile_data/', function (data) {
        var rep_data = JSON.parse(data);
        data_result = {'game_list':rep_data.game_list,
        'votes_list':rep_data.votes_list};
        if (rep_data.code != '500') {
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('main'));
            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: '17173新游期待榜'
                },
                tooltip: {},
                legend: {
                    data: ['票数']
                },
                xAxis: {
                    type: 'category',
                    data: rep_data.game_list
                },
                yAxis: {},
                series: [{
                    name: '票数',
                    type: 'bar',
                    data: rep_data.votes_list
                }]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        } else {
            layer.msg(rep_data.msg, {icon: 5});
        }


    });
}


function export_execl() {
    var href = '/echarts_excel/?data_result=' + JSON.stringify(data_result);
    $("#excel_id").attr('href', href);
}

$("#test_num input[name='x']").click(function () {
   console.log('111');
});
function abccc() {
    var checkbox = document.all('checkbox');
    console.log(checkbox);
}
$("input[name='x']").click(function () {
    console.log('1231');
});