import base64
import json
import os
import re
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import xlrd
import xlwt
from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import StreamingHttpResponse

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


# 循环文件夹下面目录并且替换内容
def replace_error(request):
    dirname = '/data/ceshi_hops/'
    try:
        for maindir, subdir, file_name_list in os.walk(dirname):
            if file_name_list:
                for f in file_name_list:
                    apath = os.path.join(maindir, f)
                    if '.py' in f and '.pyc' not in f:
                        with open(apath, 'r') as r:
                            r_value = r.readlines()
                            r.close()
                        with open(apath, 'w') as w:
                            for line in r_value:
                                if 'except Exception,e' in line or 'except Exception,e\n' in line:
                                    a = re.sub('except Exception,e', 'except Exception as e', line)
                                elif 'except Exception, e\n' in line or 'except Exception, e' in line:
                                    a = re.sub('except Exception, e', 'except Exception as e', line)
                                elif 'urllib2' in line or 'urllib2\n' in line:
                                    a = re.sub('urllib2', 'urllib.request', line)
                                elif 'import sys' in line or 'import sys\n' in line:
                                    a = re.sub('import sys', 'import importlib,sys', line)
                                elif 'reload(sys)' in line or 'reload(sys)\n' in line:
                                    a = 'importlib.reload(sys)\n'
                                elif "sys.setdefaultencoding('utf-8')" in line or "sys.setdefaultencoding('utf-8')\n" in line or 'sys.setdefaultencoding("utf-8")\n' in line or "sys.setdefaultencoding('utf8')\n" in line:
                                    a = '\n'
                                elif 'has_key' in line or 'has_key\n' in line:
                                    has_list = line.split('.has_key')
                                    if_result = has_list[0].split('if')
                                    right_value = has_list[1].split('(')[1].split(')')[0]
                                    if 'not' in has_list[0] or 'not\n' in has_list[0]:
                                        value = if_result[0] + 'if ' + right_value + ' not in' + \
                                                if_result[1].split('not')[1] + ':'
                                    elif 'and' in has_list[0] or 'and\n' in has_list[0]:
                                        left_value = has_list[0].split('and')[1]
                                        value = has_list[0].split('and')[
                                                    0] + 'and ' + right_value + ' in' + left_value + ":"
                                    else:
                                        value = if_result[0] + 'if ' + right_value + ' in' + if_result[1] + ':'
                                    a = value + '\n'
                                elif 'print ' in line or 'print \n' in line:
                                    print_value = line.split('print ')[1]
                                    print_result = line.split('print ')[0] + 'print(' + print_value.split('\n')[0] + ')'
                                    a = print_result + '\n'
                                else:
                                    a = line
                                w.write(a)
                            w.close()
    except Exception as e:
        print(e)
        return http.HttpResponse('文件读取出错,请检查')
    return http.HttpResponse('成功')


# 专门测试单独一个文件的读写操作
def alone_dir(request):
    apath = '//data/ceshi_hops/hops/hoolai/hoolai/turnover/views12.py'
    with open(apath, 'r') as r:
        r_value = r.readlines()
        r.close()
    with open(apath, 'w') as w:
        for line in r_value:
            if 'except Exception,e' in line or 'except Exception,e\n' in line:
                a = re.sub('except Exception,e', 'except Exception as e', line)
            elif 'except Exception, e\n' in line or 'except Exception, e' in line:
                a = re.sub('except Exception, e', 'except Exception as e', line)
            elif 'urllib2' in line or 'urllib2\n' in line:
                a = re.sub('urllib2', 'urllib.request', line)
            elif 'import sys' in line or 'import sys\n' in line:
                a = re.sub('import sys', 'import importlib,sys', line)
            elif 'reload(sys)' in line or 'reload(sys)\n' in line:
                a = 'importlib.reload(sys)\n'
            elif "sys.setdefaultencoding('utf-8')" in line or "sys.setdefaultencoding('utf-8')\n" in line or 'sys.setdefaultencoding("utf-8")\n' in line or "sys.setdefaultencoding('utf8')\n" in line:
                a = '\n'
            elif 'has_key' in line or 'has_key\n' in line:
                has_list = line.split('.has_key')
                if_result = has_list[0].split('if')
                right_value = has_list[1].split('(')[1].split(')')[0]
                if 'not' in has_list[0] or 'not\n' in has_list[0]:
                    value = if_result[0] + 'if ' + right_value + ' not in' + \
                            if_result[1].split('not')[1] + ':'
                elif 'and' in has_list[0] or 'and\n' in has_list[0]:
                    left_value = has_list[0].split('and')[1]
                    value = has_list[0].split('and')[
                                0] + 'and ' + right_value + ' in' + left_value + ":"
                else:
                    value = if_result[0] + 'if ' + right_value + ' in' + if_result[1] + ':'
                a = value + '\n'
            elif 'print ' in line or 'print \n' in line:
                print_value = line.split('print ')[1]
                print_result = line.split('print ')[0] + 'print(' + print_value.split('\n')[0] + ')'
                a = print_result + '\n'
            else:
                a = line
            w.write(a)
        w.close()
    return http.HttpResponse('成功')

@user_login
def excel_input(request):
    """
    根据前端传入的excel文件进行解析
    并且将解析出来的数据返回页面
    :param request:
    :return:
    """
    files = request.FILES.get('file')
    tempFilePath = files.read()
    excel = xlrd.open_workbook(file_contents=tempFilePath)
    # excel.sheet_names()  # 获取excel里的工作表sheet名称数组
    sheet = excel.sheet_by_index(0)  # 根据下标获取对应的sheet表

    # sheet.row_values(0)  # 获取第一行的数据
    # sheet.col_values(0)  # 获取第一列的数据
    nrows = sheet.nrows  # 获取总共的行数
    ncols = sheet.ncols  # 获取总共的列数

    excel_list = []
    for i in range(nrows):
        nrows_dict = {}
        # 获取所有行的数据
        nrow_value = sheet.row_values(i)
        if i == 0:
            rows_list = nrow_value
        else:
            for j in range(ncols):
                # 获取每行第几列的数据
                ncols_value = nrow_value[j]
                nrows_dict['num' + str(j)] = ncols_value
            excel_list.append(nrows_dict)
    num_list = []
    for n in range(ncols):
        num_list.append('num' + str(n))


    return render(request, 'excel.html', locals())

@login_required()
def excel_download(request):
    # 创建一个xlwt对象
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个excel的sheet
    worksheet = workbook.add_sheet('sheet')
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = '宋体'
    font.bold = True  # 黑体
    font.underline = True  # 下划线
    font.italic = True  # 斜体字
    style.font = font  # 设定样式
    worksheet.write(0, 0, '4444')  # 不带样式的写入
    worksheet.write(2, 0, '1111')
    worksheet.write(3, 0, '2222')
    worksheet.write(1, 0, '2222')

    # worksheet.write(1, 0, '5555', style)  # 带样式的写入
    file_out = '/data/file.xls'
    workbook.save(file_out)  # 保存文件

    # 使用方法返回一个excel文件
    response = StreamingHttpResponse(file_open(file_out))
    # 返回页面上显示的excel文字
    response['Content_Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format('111.xls')
    return response

def file_open(file_out):
    with open(file_out, 'rb') as f:
        while True:
            c = f.read()
            if c:
                yield c
            else:
                break