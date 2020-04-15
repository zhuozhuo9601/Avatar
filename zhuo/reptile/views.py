import json
import os
from io import BytesIO

from bs4 import BeautifulSoup

from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render

# Create your views here.
from pip._vendor import requests
from xlwt import Workbook


def reptile_index(request):
    """
    进入爬虫页面
    :param request:
    :return:
    """
    return render(request, 'reptile.html')


def reptile_data(request):
    html_text = 'https://www.17173.com/'
    res_dict = {'code': '200'}
    try:
        r = requests.get(html_text)
        r.encoding = 'utf-8'
        demo = r.text
        bs = BeautifulSoup(demo, "html.parser")
        data = bs.select('#forsetLink81 > div.rank-bd.rank-load-newgamelist > ul > li')
        # forsetLink83 > div.rank-bd.rank-load-newgamelist > ul > li.item.active
        game_list = []
        votes_list = []
        # for l in li:
        #     game_dict = {}
        #     game_name = l.find('div', {'class': 'C2'})
        #     game_number = l.find('div', {'class': 'C1'})
        #     if game_name and game_number:
        #         game_dict['num'] = game_number
        #         game_dict['name'] = game_name
        #     if game_dict:
        #         game_list.append(game_dict)
        # res_dict['msg'] = '爬取成功'
        # res_dict['data'] = game_list
        for i in data:
            c1 = i.find('div', {'class': 'c1'})
            if c1:
                c1_data = c1.get_text()
            c2 = i.find('div', {'class': 'c2'}).find('a')
            if c2:
                c2_data = c2.get_text()
            c4 = i.find('div', {'class': 'c4'})
            if c4:
                c4_data = c4.get_text()
            if c1 and c2 and c4:
                game_list.append(c2_data)
                votes_list.append(c4_data)
        if game_list and votes_list:
            res_dict['game_list'] = game_list
            res_dict['votes_list'] = votes_list
        return HttpResponse(json.dumps(res_dict))
    except Exception as e:
        res_dict['code'] = '500'
        res_dict['msg'] = '爬取数据出错,请重新点击或者稍等重试'
        return HttpResponse(json.dumps(res_dict))


def echarts_excel(request):
    ws = Workbook(encoding='utf-8')
    # 创建sheet名称
    w = ws.add_sheet(u"数据报表第一页")
    # 创建一行数据
    w.write(0, 0, "id")
    w.write(0, 1, u"用户名")
    w.write(0, 2, u"发布时间")
    w.write(0, 3, u"内容")
    w.write(0, 4, u"来源")
    # 写入数据

    # 检测文件是否存在
    exist_file = os.path.isfile("/home/python/Desktop/excel/test.xls")
    if exist_file:
        os.remove(r"/home/python/Desktop/excel/test.xls")
    ws.save("/home/python/Desktop/excel/test.xls")
    sio = BytesIO()
    ws.save(sio)
    sio.seek(0)
    try:
        response = StreamingHttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=test.xls'
        return response
    except Exception as e:
        return HttpResponse('下载文件失败')
