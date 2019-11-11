import json
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django import http

from django.shortcuts import render

# Create your views here.
from text.base import user_login


@user_login
def study_first(request):
    return render(request, 'study.html')


# 发送邮件
@user_login
def send(request):
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
