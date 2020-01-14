"""
Django settings for zhuo project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#(ae-0^u2djwyyp)jnncc7k@2iy&=z(5uq^w1+v9^+ry704%4x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'text',
    'study',
    'seriali',
    'rest_framework',
    'fontend',
)

MIDDLEWARE_CLASSES = (
    # 配置全站缓存
    # 'django.middleware.cache.UpdateCacheMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 我自己用来测试的中间件
    'system.middle.customMiddleware2',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    # 配置全站缓存
    # 'django.middleware.cache.FetchFromCacheMiddleware',
)

#设置缓存的生命周期，若在缓存配置CACHES中设置TIMEOUT属性，则程序优先选择这里的设置
# CACHE_MIDDLEWARE_SECONDS = 15
#设置缓存数据保存在数据表my_cache_table中，属性值default来自于缓存配置CACHES的default属性
# CACHE_MIDDLEWARE_ALIAS = 'default'
#设置缓存表字段cache_key的值，用于同一个Django项目多个站点之间的共享缓存
# CACHE_MIDDLEWARE_KEY_PREFIX = 'mysite'

ROOT_URLCONF = 'zhuo.urls'

# 增加admin站点管理和DRF框架的时候需要使用django模板
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.join(BASE_DIR, 'templates')]
#         ,
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]
# 使用vue的时候使用jinja
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',#修改1
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS':True,
        'OPTIONS':{
            'environment':'utils.jiaja2_env.jinja2_environment',# 修改2
            'context_processors':[
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'zhuo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'mysql',  # 数据库用户密码
        'NAME': 'django_zhuo'  # 数据库名字
    }
}

#BACKEND用于配置缓存引擎，LOCATION用于数据表的命名
CACHES = {
    # 'default':{
    #     'BACKEND':'django.core.cache.backends.db.DatabaseCache',
    #     'LOCATION':'mysite_text_city',
    #     #设置缓存的生命周期，以秒为单位，若为None，则永不过期
    #     'TIMEOUT': 60,
    #     'OPTIONS':{
    #         #MAX_ENTRIES代表最大缓存记录的数量
    #         'MAX_ENTRIES': 1000,
    #         #当缓存到达最大数量之后，设置剔除缓存的数量
    #         'CULL_FREQUENCY': 3,
    #     }
    # },

    # redis库存储缓存
     "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PASSWORD": "django_redis"
            }
        },
    # 设置多个缓存数据表
#     'mysite':{
#         'BACKEND':'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION':'mysite_text_city',
# }
    # 忘记密码返回邮箱
    "email_code": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://127.0.0.1:6379/2",
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
           }
       },
}

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
AUTH_USER_MODEL = 'text.User'
youxiangmima = 'zhuozhuo9601'

# celery异步
# BROKER_URL = 'redis://:django_redis@localhost:6379/2'
CELERY_BROKER_URL = 'redis://:django_redis@localhost:6379/3'
CELERY_RESULT_BACKEND = 'redis://:django_redis@localhost:6379/3'

# 登陆访问限制必须登陆状态,配置 LOGIN_URL 参数
LOGIN_URL = '/login/'