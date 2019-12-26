import base64
import json
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator

from django.shortcuts import render

# Create your views here.
from study.models import Community, Comment, UserLike
from system.tasks import celery_value
from text.base import user_login
from text.models import User
from zhuo import settings


@user_login
def study_first(request):
    return render(request, 'study.html')


# 发送邮件
@user_login
def send(request):
    """
    邮件功能
    :param request:
    :return:
    """
    # 发件人
    sender = request.POST.get('username')
    # 接收者
    receiver = request.POST.get('receiver')
    # 邮件服务器
    smtpserver = 'smtp.163.com'
    username = request.POST.get('username')
    password = request.POST.get('password')
    theme = request.POST.get('theme')
    mail_title = theme

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = Header(mail_title, 'utf-8')

    # 邮件正文内容
    content = request.POST.get('content')
    message.attach(MIMEText(content, 'plain', 'utf-8'))

    smtpObj = smtplib.SMTP()  # 注意：如果遇到发送失败的情况（提示远程主机拒接连接），这里要使用SMTP_SSL方法
    smtpObj.connect(smtpserver)
    smtpObj.login(username, password)
    smtpObj.sendmail(sender, receiver, message.as_string())
    print("邮件发送成功！！！")
    smtpObj.quit()
    return http.HttpResponse('200')


# 测试函数
def study_text(request):
    print('123')
    return http.HttpResponse('必须有一个返回值，或者使用ajax')


# 测试函数
def study_json(request):
    post = request.body
    data = post.decode()
    json_data = json.loads(data)
    print(json_data)
    return http.HttpResponse('测试前端发送json数据接收')


# 忘记密码跳转页面
def forget(request):
    # 在虚拟机测试可以打开，服务器不打开，用来测试celery异步任务的
    # c = celery_value.delay(1,3)
    # print(c)
    return render(request, 'forget.html', locals())


# 忘记密码发送邮箱
def forget_email(request):
    """
    邮件功能
    :param request:
    :return:
    """
    response_dict = {'code': '', 'message': ''}
    try:
        email_dict = json.loads(request.body.decode())
        # 发件人
        sender = 'fanlizhuoflz@163.com'
        username = 'fanlizhuoflz@163.com'
        password = settings.youxiangmima
        # 接收者
        receiver = email_dict.get('email')
        # 邮件服务器
        smtpserver = 'smtp.163.com'
        account = email_dict.get('username')
        if account:
            user_object = User.objects.filter(username=account)
            if not user_object:
                return http.HttpResponse('账号不存在')
        theme = '忘记密码邮件'
        mail_title = theme

        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = Header(mail_title, 'utf-8')

        # 邮件正文内容
        # 编码： 字符串 -> 二进制 -> base64编码
        # b64_name = base64.b64encode(account.encode())
        # b'546L5aSn6ZSk'
        # 解码：base64编码 -> 二进制 -> 字符串
        # print(base64.b64decode(b64_name).decode())

        content = 'http://127.0.0.1:8001/forget_password/' + account
        message.attach(MIMEText(content, 'plain', 'utf-8'))

        smtpObj = smtplib.SMTP()  # 注意：如果遇到发送失败的情况（提示远程主机拒接连接），这里要使用SMTP_SSL方法
        smtpObj.connect(smtpserver)
        smtpObj.login(username, password)
        smtpObj.sendmail(sender, receiver, message.as_string())
        smtpObj.quit()
        response_dict['code'] = '200'
        response_dict['message'] = '邮件发送成功'
        return http.HttpResponse(json.dumps(response_dict))
    except Exception as e:
        response_dict['code'] = '500'
        response_dict['message'] = '邮件发送失败'
        return http.HttpResponse(json.dumps(response_dict))


# 忘记密码进入页面
def forget_password(request, name):
    if name:
        return render(request, 'forget_password.html')


# 忘记密码输入密码页面
def set_password(request):
    json_dict = json.loads(request.body.decode())
    password1 = json_dict['password1']
    password2 = json_dict['password2']
    name = json_dict['name']
    # username = base64.b64decode(name).decode()
    response_dict = {'code': '', 'message': ''}
    if password1 == password2:
        try:
            user = User.objects.get(username=name)
            # 调用方法修改密码
            user.password = make_password(password1)
            user.save()
            response_dict['code'] = '200'
            response_dict['message'] = '重置密码成功'
        except Exception as e:
            response_dict['code'] = '500'
            response_dict['message'] = '没有这个用户'
            return http.HttpResponse(json.dumps(response_dict))
        return http.HttpResponse(json.dumps(response_dict))
    else:
        response_dict['code'] = '500'
        response_dict['message'] = '两次密码不正确'
        return http.HttpResponse(json.dumps(response_dict))


# 修改密码页面
def modify_password(request):
    return render(request, 'modify.html')


# 修改密码更新密码
def update_password(request):
    modify_dict = json.loads(request.body.decode())
    response_dict = {'code': '', 'message': ''}
    if modify_dict:
        try:
            username = modify_dict.get('username')
            password = modify_dict.get('password1')
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            response_dict['code'] = '200'
            response_dict['message'] = '修改密码成功'
            return http.HttpResponse(json.dumps(response_dict))
        except Exception as e:
            response_dict['code'] = '500'
            response_dict['message'] = '修改密码失败'
            return http.HttpResponse(json.dumps(response_dict))
    else:
        response_dict['code'] = '500'
        response_dict['message'] = '修改密码失败'
        return http.HttpResponse(json.dumps(response_dict))


# 进入社区页面
@login_required
def community(request):
    username = request.user
    try:
        user = User.objects.get(username=username)
        community_object = Community.objects.all().values('id', 'user', 'title', 'content', 'like')
        for key, count_id in enumerate(community_object):
            counts = Comment.objects.filter(comm=str(count_id['id'])).count()
            community = Community.objects.get(id=count_id['id'])
            user_like = UserLike.objects.filter(user=user, community=community).values('like_status').first()
            if counts == 0:
                community_object[key]['count'] = '添加'
            else:
                community_object[key]['count'] = str(counts) + '条'
            if count_id['like'] == 0:
                community_object[key]['like'] = '赞同'
            else:
                if user_like:
                    if user_like['like_status'] == '0':
                        community_object[key]['like'] = '赞同' + str(count_id['like'])
                    else:
                        community_object[key]['like_status'] = '这个赞同过了'
                        community_object[key]['like'] = '已赞同' + str(count_id['like'])
                else:
                    community_object[key]['like'] = '赞同' + str(count_id['like'])
        return render(request, 'community.html', locals())
    except Exception as e:
        return render(request, 'error_404_500.html')


# 评论返回数据
@user_login
def comment(request):
    """
    :param current_page: 用户请求的当前页
    :param total_count:  数据库中查询到的数据总条数
    :param base_url:    请求的 url 路径
    :param per_page_count: 每页显示的数据条数
    :param max_pager_num: 页面上最多显示的页码
    """
    id_dict = json.loads(request.body.decode())
    json_dict = {'code': '1', 'msg': '成功'}
    id = id_dict.get('id', '')
    page = id_dict.get('page', '')
    status = id_dict.get('status', '')
    if id:
        try:
            com_object = Comment.objects.filter(comm=str(id))
            data_list = []
            # 创建分页器
            pageTotal = Paginator(com_object, 2)
            # 页数的列表
            page_list = pageTotal.page_range
            # 判断当前页面是否比总页数大
            if int(page) > pageTotal.num_pages:
                page = pageTotal.num_pages
            # 获取第page页的数据
            com_page = pageTotal.page(page)
            # 判断当前页是否有下一页，如果有　返回true,没有返回false
            if com_page.has_next():
                # 如果有下一页则获取下一页的页码
                has_next = com_page.next_page_number()
                json_dict['has_next'] = has_next
            else:
                json_dict['has_next'] = '0'
            # 判断当前页是否有上一页，如果有　返回true,没有返回false
            if com_page.has_previous():
                has_previous = com_page.previous_page_number()
                json_dict['has_previous'] = has_previous
            else:
                json_dict['has_previous'] = '0'
            json_dict['page_list'] = list(page_list)
            for result in com_page:
                mk_dict = {}
                mk_dict['username'] = result.com_user.username
                mk_dict['comment'] = result.comment
                data_list.append(mk_dict)
            json_dict['data'] = data_list
            json_dict['status'] = status
        except Exception as e:
            json_dict['code'] = '0'
            json_dict['msg'] = '加载文章评论失败'
        return http.HttpResponse(json.dumps(json_dict))
    else:
        json_dict['code'] = '0'
        json_dict['msg'] = '请选择文章'
        return http.HttpResponse(json.dumps(json_dict))


# 储存用户写的评论
@user_login
def comm_store(request):
    data_dict = json.loads(request.body.decode())
    json_dict = {'code': '1', 'msg': '成功'}
    if data_dict:
        try:
            c_object = Community.objects.get(id=data_dict['id'])
            Comment.objects.create(comm=c_object, com_user=c_object.user, comment=data_dict['text'])
        except Exception as e:
            json_dict['code'] = '0'
            json_dict['msg'] = '填写评论出错，请重试'
        return http.HttpResponse(json.dumps(json_dict))
    else:
        json_dict['code'] = '0'
        json_dict['msg'] = '请填写评论'
        return http.HttpResponse(json.dumps(json_dict))


# 用户点赞
@user_login
def comm_like(request):
    id = json.loads(request.body.decode())
    like_dict = {'code': '1'}
    user = request.user
    if id:
        try:
            comm_object = Community.objects.get(id=id)
            user_like = UserLike.objects.filter(community__id=id, user__username=user)
            if user_like:
                for likes in user_like:
                    community = likes.community
                    if likes.like_status == '0':
                        like_dict['like_status'] = '这个已经赞同过了'
                        like_dict['like'] = '已赞同' + str(community.like + 1)
                        likes.like_status = '1'
                        likes.save()
                        community.like = community.like + 1
                        community.save()
                    else:
                        if community.like - 1 == 0:
                            like_dict['like'] = '赞同'
                        else:
                            like_dict['like'] = '赞同' + str(community.like - 1)
                        likes.like_status = '0'
                        likes.save()
                        community.like = community.like - 1
                        community.save()
            else:
                like_dict['like_status'] = '这个已经赞同过了'
                like_dict['like'] = '已赞同' + str(comm_object.like + 1)
                UserLike.objects.create(user=user, community=comm_object, like_status='1')
                comm_object.like = comm_object.like + 1
                comm_object.save()

            return http.HttpResponse(json.dumps(like_dict))
        except Exception as e:
            like_dict['code'] = '0'
            like_dict['like'] = '文章点赞出错了'
            return http.HttpResponse(json.dumps(like_dict))
    else:
        like_dict['code'] = '0'
        like_dict['like'] = '请选择一个文章点赞'
        return http.HttpResponse(json.dumps(like_dict))


# 这是如果出现404或者500的错误返回一个错误的页面
@user_login
def error_404(request):
    return render(request, 'error_404_500.html')
