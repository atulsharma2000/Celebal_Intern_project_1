from django.db import models

from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
