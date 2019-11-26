import json
import re

import datetime

from decimal import Decimal

from django import http
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Permission
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from text.base import user_login
from text.models import User, Image, ImageDetails, UserDetails, UserCity


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


# @method_decorator(user_login, name="get")
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
        json_dict = {'code': '0', 'msg': ''}
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]{4,15}$', username):
            json_dict['msg'] = '用户名不符合规则'
            data = json.dumps(json_dict)
            return http.HttpResponse(data)
        if not re.match(r'^[0-9A-Za-z]{6,20}$', password):
            json_dict['msg'] = '密码不符合规则'
            data = json.dumps(json_dict)
            return http.HttpResponse(data)
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            json_dict['msg'] = '手机号不符合规则'
            data = json.dumps(json_dict)
            return http.HttpResponse(data)
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
            json_dict['code'] = '1'
            json_dict['msg'] = '注册成功'
            data = json.dumps(json_dict)
            return http.HttpResponse(data)
        except Exception as e:
            json_dict['msg'] = '注册失败'
            data = json.dumps(json_dict)
            return http.HttpResponse(data)


# @method_decorator(user_login, name='get')
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
                return http.HttpResponse('0')


class IndexView(View):
    """
    首页
    """

    def get(self, request):
        user = request.user.username
        if user:
            user_data = UserDetails.objects.filter(user_id__username=user).values('username')
            if user_data:
                username = user_data[0].get('username')
            else:
                username = '路人'
        return render(request, 'index.html', locals())


@method_decorator(user_login, name='get')
class UserView(View):
    """
    信息图片展示页面
    """

    def get(self, request):
        username = request.user.username
        if username:
            if username == 'lizhuo01':
                user_admin = 'lizhuo01'
            user_data = User.objects.get(username=username)
            # 增加用户权限
            # permiss = Permission.objects.get(id=1)
            # user_data.user_permissions.add(permiss)
            # user_per = user_data.get_all_permissions()
            province = UserCity.objects.filter(mark_id=1).values_list('id', 'city')
            img = Image.objects.filter(ima_name=user_data.id).values('id', 'img_url', 'content_one', 'content_two')
            details = UserDetails.objects.filter(user_id__username=username).values('username', 'sex', 'city',
                                                                                    'province', 'area', 'sign', 'hobby',
                                                                                    'birthday', 'career')
            if details:
                details_username = details[0].get('username')
            else:
                details_username = '路人'
            return render(request, 'user.html', locals())
        else:
            return redirect(reverse("texts:login"))

    def post(self, request):
        id = request.POST.get('id')
        json_dict = {'code': '0', 'msg': '图片显示失败'}
        if id:
            try:
                image = ImageDetails.objects.get(details_id=id)
                imageData = {"images": '../' + str(image.images), "content_one": image.details_one,
                             "content_two": image.details_two}
                json_dict['code'] = '1'
                json_dict['msg'] = '图片显示成功'
                json_dict['images'] = imageData
                data = json.dumps(json_dict)
                return http.HttpResponse(data)
            except Exception as e:
                data = json.dumps(json_dict)
                return http.HttpResponse(data)


@method_decorator(user_login, name='post')
class UserAdd(View):
    """
    个人资料添加
    """

    def post(self, request):
        add_dict = json.loads(request.body.decode())
        user = request.user.username
        json_dict = {'code': '', 'msg': ''}
        try:
            if add_dict and user:
                create_dict = {}
                for key in add_dict:
                    if add_dict[key] and len(add_dict[key]) < 30:
                        create_dict[key] = add_dict[key]
                user_object = User.objects.get(username=user)
                userdetails = UserDetails.objects.update_or_create(user_id=user_object, defaults=create_dict)
                json_dict['code'] = '1'
                json_dict['msg'] = '添加成功'
                data = json.dumps(json_dict)
                return http.HttpResponse(data)
        except Exception as e:
            json_dict['code'] = '0'
            json_dict['msg'] = '添加失败'
            data = json.dumps(json_dict)
            return http.HttpResponse(data)


@method_decorator(user_login, name='post')
class ImageView(View):
    """
    图片上传功能
    """

    def post(self, request):
        if request.FILES.get('file'):
            img = request.FILES.get('file')
            try:
                username = request.user.username
                if img:
                    user = User.objects.get(username=username)
                    Image.objects.create(img_url=img, content_one='系列', content_two='...', ima_name=user)
                    return http.HttpResponse('图片上传成功')
            except Exception as e:
                return http.HttpResponse('图片上传失败')
        else:
            return http.HttpResponse('请选择一个图片')


@method_decorator(user_login, name='get')
class AboutView(View):
    """
    首页跳转其他页面
    """

    def get(self, request):
        return render(request, 'about.html')


@method_decorator(user_login, name='get')
class GamesView(View):
    """
    首页跳转其他页面
    """

    def get(self, request):
        return render(request, 'games.html')


@method_decorator(user_login, name='get')
class NewsView(View):
    """
    首页跳转其他页面
    """

    def get(self, request):
        return render(request, 'news.html')


@method_decorator(user_login, name='get')
class ContactView(View):
    """
    首页跳转其他页面
    """

    def get(self, request):
        return render(request, 'contact.html')


@method_decorator(user_login, name='get')
class SingleView(View):
    """
    首页跳转其他页面
    """

    def get(self, request):
        return render(request, 'single.html')


@method_decorator(user_login, name='get')
class TableView(View):
    """
    个人资料展示页
    """

    def get(self, request):
        return render(request, 'table.html', locals())

    def post(self, request):
        user = UserDetails.objects.all().values('id', 'username', 'province', 'sex', 'hobby', 'city', 'sign',
                                                'birthday', 'career', 'area')
        paginator = Paginator(user, 10)
        page = request.POST.get('page', 1)
        paginator_data = paginator.page(page)
        user_list = []
        for user_data in paginator_data:
            if user_data['birthday']:
                user_data['birthday'] = user_data['birthday'].strftime('%Y-%m-%d')
            user_list.append(user_data)
        user_dict = {'code': '0', 'msg': '表格数据刷新成功', 'data': user_list}
        data = json.dumps(user_dict, cls=ComplexEncoder)
        return http.HttpResponse(data)


@method_decorator(user_login, name='post')
class TableAdd(View):
    """
    个人资料添加
    """

    def post(self, request):
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


@method_decorator(user_login, name='post')
class TableUpdate(View):
    """
    个人资料修改
    """

    def post(self, request):
        update_dict = request.POST.getlist('update_dict')
        update_list = update_dict[0]
        update_data = json.loads(update_list)
        for data in list(update_data.keys()):
            if not update_data.get(data):
                del update_data[data]
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


@method_decorator(user_login, name='post')
class TableDelete(View):
    """
    个人资料删除
    """

    def post(self, request):
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


@method_decorator(user_login, name='get')
class EchartsView(View):
    """
    柱状图，饼图等显示
    """

    def get(self, request):
        return render(request, 'echarts.html')


class OutLogin(View):
    """
    退出登陆功能
    """

    def get(self, request):
        logout(request)
        response = redirect(reverse('texts:login'))
        # 清除cookie数据
        # response.set_cookie()
        response.delete_cookie('username')
        return response


class UserProvince(View):
    """
    省市区三级联动
    """

    def post(self, request):
        id_list = request.POST.getlist('id')
        id = id_list[0]
        if id:
            city_list = []
            user_data = UserCity.objects.filter(Subordinate_id=id).values_list('id', 'city')
            for key, value in user_data:
                if key and value:
                    city_dict = {}
                    city_dict['id'] = key
                    city_dict['city'] = value
                    city_list.append(city_dict)
        city_data = json.dumps(city_list, cls=ComplexEncoder)
        return http.HttpResponse(city_data)
