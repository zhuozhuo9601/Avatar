from haystack import indexes

from df_goods.models import Note


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)  # 创建一个text字段
    # 对标题，简介，内容进行搜索
    author = indexes.CharField(model_attr='user')
    pub_date = indexes.DateTimeField(model_attr='pub_date')


    def get_model(self):
        return Note

    def index_queryset(self, using=None):
        return self.get_model().objects.all()