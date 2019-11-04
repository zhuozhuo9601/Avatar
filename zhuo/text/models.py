from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """自定义用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Image(models.Model):
    img_url = models.ImageField(upload_to='static/userimages')  # upload_to指定图片上传的途径，如果不存在则自动创建
    content_one = models.CharField(max_length=200, blank=True)
    content_two = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'tb_image'


class ImageDetails(models.Model):
    details_id = models.ForeignKey("Image", to_field="id", null=True, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='static/userimages')
    details_one = models.CharField(max_length=200, blank=True)
    details_two = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'tb_details'
