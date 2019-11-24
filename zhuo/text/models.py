from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
from system.storage import ImageStorage


class User(AbstractUser):
    """自定义用户模型类"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    year = models.CharField(max_length=11,null=True)
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Image(models.Model):
    """图片上传模型类"""
    ima_name = models.ForeignKey(User,max_length=20,null=True)
    img_url = models.ImageField(upload_to='static/userimages',storage=ImageStorage())  # upload_to指定图片上传的途径，如果不存在则自动创建
    content_one = models.CharField(max_length=200, blank=True)
    content_two = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'tb_image'


class ImageDetails(models.Model):
    """图片详情模型类"""
    details_id = models.ForeignKey("Image", to_field="id", null=True, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='static/userimages')
    details_one = models.CharField(max_length=200, blank=True)
    details_two = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'tb_details'

class UserDetails(models.Model):
    """个人信息详情模型类"""
    user_id = models.ForeignKey("User", to_field="id", null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    experience = models.IntegerField()
    sex = models.CharField(max_length=10)
    score = models.IntegerField()
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=100, null=True)
    sign = models.CharField(max_length=200)
    classify = models.CharField(max_length=200)
    wealth = models.IntegerField()
    time = models.DateField(null=True)
    class Meta:
        db_table = 'text_userdetails'

class UserCity(models.Model):
    """省市区三级联动"""
    city = models.CharField(max_length=50)
    Subordinate_id = models.IntegerField(null=True)
    mark_id = models.IntegerField(null=True)
    class Meta:
        db_table = 'text_city'