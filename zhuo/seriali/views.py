from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from seriali.models import BookInfo
from seriali.serializer import BookInfoSerializer


class BookInfoViewSet(ModelViewSet):
    # 查询集
    queryset = BookInfo.objects.all()
    # 返回序列化器
    serializer_class = BookInfoSerializer

    # detail为False 表示不需要处理具体的BookInfo对象
    @action(methods=['get'], detail=False)
    def latest(self, request):
        """
        返回最新的图书信息
        """
        # latest最近的一条数据
        book = BookInfo.objects.latest('id')
        serializer = self.get_serializer(book)
        return Response(serializer.data)