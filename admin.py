from django.contrib import admin

# Register your models here.
# from blog.models import Article
from .models import Article, SignUp, Comments

admin.site.register(Article)
admin.site.register(SignUp)
admin.site.register(Comments)