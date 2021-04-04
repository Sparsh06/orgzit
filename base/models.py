from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null = True, blank=True)
    email = models.CharField(max_length=50,blank=False,default=False)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) 
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']


class ShareKey(models.Model):
    location = models.TextField() # absolute path
    token = models.CharField(max_length=40, primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_seconds = models.BigIntegerField()
    