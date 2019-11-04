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

from text.models import User, Image, ImageDetails


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
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]{4,15}$', username):
            return http.HttpResponse('500')
        if not re.match(r'^[0-9A-Za-z]{6,20}$', password):
            return http.HttpResponse('500')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            # code = '0'
            # msg = '手机号不符合规则'
            # msgdata = {"code": code, "msg": msg}
            return http.HttpResponse('500')
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
            return redirect(reverse("texts:login"))
        except Exception as e:
            return render(request, 'register.html')


class LoginView(View):
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
                return http.HttpResponse('500')


class IndexView(View):
    def get(self, request):
        user = request.user.username
        if user:
            return render(request, 'index.html')
        else:
            return redirect(reverse("texts:login"))


class UserView(View):
    def get(self, request):
        username = request.user.username
        if username:
            if username == 'lizhuo01':
                user_admin = 'lizhuo01'
            img = Image.objects.all().values('id','img_url','content_one','content_two')
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
                images = json.dumps(imageData)
                return http.HttpResponse(images)
            except Exception as e:
                return http.HttpResponse('500')


class ImageView(View):
    def post(self, request):
        img = request.FILES.get('file')
        try:
            if img:
                Image.objects.create(img_url=img,content_one='系列',content_two='...')
                return http.HttpResponse('新增成功')
        except Exception as e:
            return http.HttpResponse('新增失败')