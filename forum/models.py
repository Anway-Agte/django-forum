from django.db import models
from django.contrib.auth.models import User

class Thread(models.Model):
    user = models.ForeignKey(to = User , on_delete = models.CASCADE) 
    title = models.TextField(max_length = 1000)
    content = models.TextField(max_length = 10000) 

class Comment(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    thread = models.ForeignKey(Thread , on_delete = models.CASCADE , related_name = 'comments')
    commentText = models.TextField(max_length = 1000)