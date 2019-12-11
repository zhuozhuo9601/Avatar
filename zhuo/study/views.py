import json
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django import http

from django.shortcuts import render

# Create your views here.
from study.models import Community, Comment
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
    return render(request, 'forget.html', locals())


# 忘记密码发送邮箱
def forget_email(request):
    """
    邮件功能
    :param request:
    :return:
    """
    response_dict = {'code':'','message':''}
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
        content = 'http://127.0.0.1:8001/login/'
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
        response_dict['code'] = '５00'
        response_dict['message'] = '邮件发送失败'
        return http.HttpResponse(json.dumps(response_dict))

# 修改密码页面
def forget_password(request):
    return render(request, 'forget_password.html')

# 修改密码更新密码
def forget_modify(request):
    modify_dict = json.loads(request.body.decode())
    response_dict = {'code':'','message':''}
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
def community(request):
    community_object = Community.objects.all().values('id', 'user', 'title', 'content')
    return render(request, 'community.html', locals())

# 评论返回数据
def comment(request):
    id = json.loads(request.body.decode())
    json_dict = {'code': '1', 'msg': '成功'}
    if id:
        try:
            com_object = Comment.objects.filter(comm=str(id))
            data_list = []
            for result in com_object:
                mk_dict = {}
                mk_dict['username'] = result.com_user.username
                mk_dict['comment'] = result.comment
                data_list.append(mk_dict)
            json_dict['data'] = data_list
        except Exception as e:
            json_dict['code'] = '0'
            json_dict['msg'] = '加载文章评论失败'
        return http.HttpResponse(json.dumps(json_dict))
    else:
        json_dict['code'] = '0'
        json_dict['msg'] = '请选择文章'
        return http.HttpResponse(json.dumps(json_dict))

# 储存用户写的评论
def comm_store(request):
    data_dict = json.loads(request.body.decode())
    json_dict = {'code': '1', 'msg': '成功'}
    if data_dict:
        try:
            c_object = Community.objects.get(id=data_dict['id'])
            Comment.objects.create(comm=c_object,com_user=c_object.user,comment=data_dict['text'])
        except Exception as e:
            json_dict['code'] = '0'
            json_dict['msg'] = '填写评论出错，请重试'
        return http.HttpResponse(json.dumps(json_dict))
    else:
        json_dict['code'] = '0'
        json_dict['msg'] = '请填写评论'
        return http.HttpResponse(json.dumps(json_dict))