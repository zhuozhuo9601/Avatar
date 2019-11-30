import json
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django import http

from django.shortcuts import render

# Create your views here.
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
