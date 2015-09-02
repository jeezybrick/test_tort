from django.contrib.auth.models import User
from django.db import models

# Макс.длина текста
MAX_TEXT_LEN = 20


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

    def get_short_text(self):
        if len(self.text) > MAX_TEXT_LEN:
            return self.text[:MAX_TEXT_LEN]
        else:
            return self.text


class Comments(models.Model):
    message = models.CharField(max_length=1000, blank=False)
    user = models.ForeignKey(User)
    news = models.ForeignKey(Article)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.message


class SignUp(models.Model):
    email = models.EmailField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=40, default='', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.email

'''
class AvatarUpload(models.Model):
    lol = models.ImageField(upload_to='blog/static/blog/img/avatars')
'''