import json
import re

import datetime

from decimal import Decimal

from django import http
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from text.models import User, Image, ImageDetails, UserDetails


class ComplexEncoder(json.JSONEncoder):
    """
    扩展JSON,支持datetime类型序列化
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class RegisterView(View):
    """
    注册页面
    """

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]{4,15}$', username):
            json_dict = {'code': '0', 'msg': '用户名不符合规则'}
            data = json.dumps(json_dict)
            return http.HttpResponse(data)
        if not re.match(r'^[0-9A-Za-z]{6,20}$', password):
            json_dict = {'code': '0', 'msg': '密码不符合规则'}
            data = json.dumps(json_dict)
            return http.HttpResponse(data)
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            json_dict = {'code': '0', 'msg': '手机号不符合规则'}
            data = json.dumps(json_dict)
            return http.HttpResponse(data)
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
            return redirect(reverse("texts:login"))
        except Exception as e:
            return render(request, 'register.html')


class LoginView(View):
    """
    登陆页面
    """

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                request.session.set_expiry(None)
                response = redirect(reverse('texts:index'))
                response.set_cookie('username', user.username, max_age=14 * 24 * 3600)
                return response
            else:
                json_dict = {'code': '0', 'msg': '登陆失败'}
                data = json.dumps(json_dict)
                return http.HttpResponse(data)


class IndexView(View):
    """
    首页
    """

    def get(self, request):
        user = request.user.username
        if user:
            return render(request, 'index.html')
        else:
            return redirect(reverse("texts:login"))


class UserView(View):
    """
    信息图片展示页面
    """

    def get(self, request):
        username = request.user.username
        if username:
            if username == 'lizhuo01':
                user_admin = 'lizhuo01'
            img = Image.objects.all().values('id', 'img_url', 'content_one', 'content_two')
            return render(request, 'user.html', locals())
        else:
            return redirect(reverse("texts:login"))

    def post(self, request):
        id = request.POST.get('id')
        if id:
            try:
                image = ImageDetails.objects.get(details_id=id)
                imageData = {"images": '../' + str(image.images), "content_one": image.details_one,
                             "content_two": image.details_two}
                json_dict = {'code': '1', 'msg': '图片显示成功',"images":imageData}
                data = json.dumps(json_dict)
                return http.HttpResponse(data)
            except Exception as e:
                json_dict = {'code': '0', 'msg': '图片显示失败'}
                data = json.dumps(json_dict)
                return http.HttpResponse(data)


class ImageView(View):
    """
    图片上传功能
    """

    def post(self, request):
        img = request.FILES.get('file')
        try:
            if img:
                Image.objects.create(img_url=img, content_one='系列', content_two='...')
                json_dict = {'code': '1', 'msg': '图片上传成功'}
                data = json.dumps(json_dict)
                return http.HttpResponse(data)
        except Exception as e:
            json_dict = {'code': '0', 'msg': '图片上传失败'}
            data = json.dumps(json_dict)
            return http.HttpResponse(data)


class AboutView(View):
    """
    首页跳转其他页面
    """

    def get(self, request):
        return render(request, 'about.html')


class GamesView(View):
    """
    首页跳转其他页面
    """

    def get(self, request):
        return render(request, 'games.html')


class NewsView(View):
    """
    首页跳转其他页面
    """

    def get(self, request):
        return render(request, 'news.html')


class ContactView(View):
    """
    首页跳转其他页面
    """

    def get(self, request):
        return render(request, 'contact.html')


class SingleView(View):
    """
    首页跳转其他页面
    """

    def get(self, request):
        return render(request, 'single.html')


class TableView(View):
    """
    个人资料展示页
    """

    def get(self, request):
        return render(request, 'table.html', locals())

    def post(self, request):
        user = UserDetails.objects.all().values('id', 'username', 'experience', 'sex', 'score', 'city', 'sign',
                                                'classify', 'wealth')
        user_list = []
        for user_data in user:
            user_list.append(user_data)
        user_dict = {'code': '0', 'msg': '', 'data': user_list}
        data = json.dumps(user_dict)
        return http.HttpResponse(data)

class TableAdd(View):
    """
    个人资料添加
    """
    def post(self,request):
        add_dict = request.POST.getlist('add_dict')
        add_list = add_dict[0]
        add_data = json.loads(add_list)
        user = request.user.username
        try:
            if add_data and user:
                user_id = User.objects.get(username=user)
                user_count = UserDetails.objects.filter(user_id=user_id.id).count()
                if user_count:
                    json_dict = {'code': '0', 'msg': '添加失败,资料已有'}
                    data = json.dumps(json_dict)
                    return http.HttpResponse(data)
                else:
                    add_data['user_id'] = user_id
                    UserDetails.objects.create(**add_data)
                    json_dict = {'code': '1', 'msg': '添加成功'}
                    data = json.dumps(json_dict)
                    return http.HttpResponse(data)
        except Exception as e:
            json_dict = {'code': '0', 'msg': '异常'}
            data = json.dumps(json_dict)
            return http.HttpResponse(data)

class TableUpdate(View):
    def post(self,request):
        update_dict = request.POST.getlist('update_dict')
        update_list = update_dict[0]
        update_data = json.loads(update_list)
        try:
            if update_data:
                UserDetails.objects.filter(id=update_data['id']).update(**update_data)
                json_dict = {'code': '1', 'msg': '修改成功'}
                data = json.dumps(json_dict)
                return http.HttpResponse(data)
        except Exception as e:
            json_dict = {'code': '0', 'msg': '修改错误'}
            data = json.dumps(json_dict)
            return http.HttpResponse(data)

class TableDelete(View):
    def post(self,request):
        id = request.POST.getlist('id')
        try:
            if id:
                UserDetails.objects.filter(id__in=id).delete()
                json_dict = {'code': '1', 'msg': '删除成功'}
                data = json.dumps(json_dict)
                return http.HttpResponse(data)
        except Exception as e:
            json_dict = {'code': '0', 'msg': '删除失误'}
            data = json.dumps(json_dict)
            return http.HttpResponse(data)