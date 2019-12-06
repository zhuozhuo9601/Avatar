from celery import Celery

app = Celery('tasks', backend='redis://:django_redis@localhost:6379/2', broker='redis://:django_redis@localhost:6379/2')

@app.task
def add(x, y):
   return x + y
