from django.db import models

# Create your models here.
class User(models.Model):
    '''用户表'''
    gender = (('male','男'),('female','女'))
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    phone = models.CharField(max_length=11,unique=True)
    email = models.EmailField(unique=True,null=True)
    sex = models.CharField(max_length=32,choices=gender,default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

