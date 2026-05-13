from django.db import models

import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

def media_directory_path(instance, filename):
    today = datetime.date.today()
    return 'posts/{0}/{1}/{2}'.format(today, 
                                        instance.user.username,
                                        filename)
# Create your models here.
class Post(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=["-date"])
        ]
    user = models.ForeignKey(User,
                                related_name='user_posts',
                                on_delete=models.CASCADE)
    media = models.FileField(upload_to=media_directory_path,
                             null=True,
                             blank=True)
    message = models.CharField(null=True, max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    
    def __str__(self):
        return f"{self.user.username} posted {self.message}"

class Comment(models.Model):
    user = models.ForeignKey(User,
                                related_name='user_comments',
                                on_delete=models.CASCADE)
    edited = models.BooleanField(blank=True, null=True, default=False)
    post = models.ForeignKey(Post,
                             related_name='post_comments',
                             on_delete=models.CASCADE)
    message = models.CharField(null=True, max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.user.username} \n {self.date}'

class Reply(models.Model):
    user = models.ForeignKey(User,
                                related_name='user_replies',
                                on_delete=models.CASCADE)
    message = models.CharField(null=True, max_length=255)
    date = models.DateTimeField(auto_now_add=True)