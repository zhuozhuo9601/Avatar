from haystack import indexes

from df_goods.models import Note


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    # document = True表名该字段是主要进行关键字查询的字段
    # use_template = True表示通过模板来指明索引值由哪些模型类字段组成
    text = indexes.CharField(document=True, use_template=True)  # 创建一个text字段


    def get_model(self):
        return Note

    def index_queryset(self, using=None):
        return self.get_model().objects.all()