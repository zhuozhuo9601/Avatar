from django.db import models

# Create your models here.
from django.db import models

from text.models import User


class Note(models.Model):
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    body = models.TextField()

def __unicode__(self):
    return self.title