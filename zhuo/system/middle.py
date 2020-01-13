from django.shortcuts import render


class customMiddleware2(object):
    # 当页面访问时，先从上往下执行
    def process_request(self,request):
        print("中间件:process_request2")
    def process_view(self,request,call_back,callback_args, callback_kwargs):
        print("中间件:process_view2")

    def process_exception(self, request, exception):
        print('报错')
    def process_template_response(self, request, response):
        print('process_template_response:', request)
    # def process_response(self, request, response):
    #     print('中间件:process_response', response)
    #     return render(request, "login.html")
