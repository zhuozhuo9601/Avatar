from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from haystack.views import SearchView

from zhuo.settings import HAYSTACK_SEARCH_RESULTS_PER_PAGE


class MySearchView(SearchView):
    def build_page(self):
        print('进入搜索页面：')
        # 分页重写
        context = super(MySearchView, self).extra_context()  # 继承自带的context
        try:
            page_no = int(self.request.GET.get('page', 1))
        except Exception as e:
            return HttpResponse("Not a valid number for page.")

        if page_no < 1:
            return HttpResponse("Pages should be 1 or greater.")
        a = []
        for i in self.results:
            a.append(i.object)
        paginator = Paginator(a, HAYSTACK_SEARCH_RESULTS_PER_PAGE)
        # print("--------")
        # print(page_no)
        page = paginator.page(page_no)
        print('搜索的商品信息：', page)
        return (paginator, page)

    def extra_context(self):
        context = super(MySearchView, self).extra_context()  # 继承自带的context
        context['title'] = '搜索'
        return context