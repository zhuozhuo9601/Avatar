import json
import os
from io import BytesIO

from io import StringIO
from bs4 import BeautifulSoup
from django.http import FileResponse

from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render

# Create your views here.
from pip._vendor import requests
from redis import StrictRedis
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
            redis = StrictRedis(host='localhost', port=6379, db=0, password='django_redis')
            for game_data, votes_data in zip(game_list, votes_list):
                num = game_list.index(game_data)
                redis.set('name'+str(num), game_data)
                redis.set('votes'+str(num), votes_data)
            res_dict['game_list'] = game_list
            res_dict['votes_list'] = votes_list
        return HttpResponse(json.dumps(res_dict))
    except Exception as e:
        res_dict['code'] = '500'
        res_dict['msg'] = '爬取数据出错,请重新点击或者稍等重试'
        return HttpResponse(json.dumps(res_dict))



def echarts_excel(request):
    data_result = json.loads(request.GET.get('data_result'))
    ws = Workbook(encoding='utf-8')
    # 创建sheet名称
    w = ws.add_sheet(u"数据报表第一页")
    # 创建一行数据
    w.write(0, 0, "游戏名称")
    w.write(0, 1, "票数")

    # 写入数据
    for i in range(len(data_result['game_list'])):
        w.write(i+1, 0, data_result['game_list'][i])
        w.write(i+1, 1, data_result['votes_list'][i])

    # 检测文件是否存在
    file_name = "/home/python/Desktop/excel/test.xls"
    exist_file = os.path.isfile(file_name)
    if exist_file:
        os.remove(file_name)
    ws.save(file_name)
    try:
        # response = StreamingHttpResponse(open(file_name), 'rb')
        # response['content_type'] = "application/octet-stream"
        # response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(file_name)
        # return response
        response = FileResponse(open(file_name, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_name)
        return response
    except Exception as e:
        return HttpResponse('下载文件失败')

def open_file(file, chunk_size=512):
    with open(file, encoding = 'gb2312') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
