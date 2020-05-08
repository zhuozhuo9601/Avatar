from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# from haystack.views import SearchView
# from elasticsearch import Elasticsearch

# from haystack.generic_views import SearchView
#
# from df_goods.models import Note
# from zhuo import settings
# from zhuo.settings import HAYSTACK_SEARCH_RESULTS_PER_PAGE

# def NewsSearchView(request):
"""
无法在虚拟环境下使用elasticsearch
"""
#     es = Elasticsearch({"192.168.222.156:9200"})
#     ret = es.search(index="csdnblog2"
#                     , body={
#             "query": {
#                 "term": {"pageContent": "cluster"}
#             }
#         }
#                     )
#     resultback = ret["hits"]["hits"]
#     context_rs = {"results": resultback}
#     return render(request, 'search/search.html', context_rs)
