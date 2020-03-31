import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.http import HttpResponse

from system.celerys import app


@app.task
def celery_value(a, b):
    """
    celery启动命令:  celery -A system.celerys worker -l info
    :param a:
    :param b:
    :return:
    """
    c = a + b

    return c

# celery发送邮件
@app.task
def send():
    """
    邮件功能
    :param request:
    :return:
    """
    # 发件人
    sender = 'fanlizhuoflz@163.com'
    # 接收者
    receiver = '664674709@qq.com'
    # 邮件服务器
    smtpserver = 'smtp.163.com'
    username = 'fanlizhuoflz@163.com'
    password = 'zhuozhuo9601'
    theme = '我来看看未来架构师'
    mail_title = theme

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = Header(mail_title, 'utf-8')

    # 邮件正文内容
    content = '充满荆棘的道路上总会有一个未来架构师'
    message.attach(MIMEText(content, 'plain', 'utf-8'))

    smtpObj = smtplib.SMTP()  # 注意：如果遇到发送失败的情况（提示远程主机拒接连接），这里要使用SMTP_SSL方法
    smtpObj.connect(smtpserver)
    smtpObj.login(username, password)
    smtpObj.sendmail(sender, receiver, message.as_string())
    smtpObj.quit()
    return "邮件发送成功！！！"