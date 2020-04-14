import json

from bs4 import BeautifulSoup

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from pip._vendor import requests


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