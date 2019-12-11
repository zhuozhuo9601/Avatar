from django.db import models

# Create your models here.
from text.models import User


# 文章表
class Community(models.Model):
    user = models.ForeignKey(User, max_length=20, null=True)
    title = models.CharField(max_length=200, null=True)
    content = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = 'tb_community'


# 评论表
class Comment(models.Model):
    comm = models.ForeignKey(Community, max_length=20, null=True)
    com_user = models.ForeignKey(User, max_length=20, null=True)
    comment = models.CharField(max_length=1000, null=True)

    class Meta:
        db_table = 'tb_comment'