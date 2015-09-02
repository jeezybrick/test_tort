__author__ = 'Jeezy'

from django.conf.urls import include, url

urlpatterns = [
    url(r"^$", 'blog.views.home', name='home'),
    url(r"^about/$", 'blog.views.about', name='about'),
    url(r"^contact/$", 'blog.views.contact', name='contact'),
    url(r"^news/$", 'blog.views.news', name='news'),
    url(r"^my/$", 'blog.views.my_show', name='my_show'),
    url(r"^my/news/$", 'blog.views.my_news', name='my_news'),
    url(r"^my/edit/$", 'blog.views.my_edit', name='my_edit'),
    url(r"^my/edit/avatar/$", 'blog.views.my_edit_avatar', name='my_edit_avatar'),
    url(r"^my/edit/avatar/success/$", 'blog.views.my_edit_avatar_success', name='my_edit_avatar_success'),
    url(r"^my/delete/$", 'blog.views.my_delete', name='my_delete'),
    url(r"^auth/login/$", 'blog.views.get_login', name='get_login'),
    url(r"^auth/post_login/$", 'blog.views.post_login', name='post_login'),
    url(r"^auth/logout/$", 'blog.views.get_logout', name='get_logout'),
    url(r"^auth/success/$", 'blog.views.login_success', name='login_success'),
    url(r"^auth/register/$", 'blog.views.get_register', name='get_register'),
    url(r"^auth/register/success/$", 'blog.views.register_success', name='register_success'),
    url(r"^articles/(?P<article_id>[0-9]+)/$", 'blog.views.show_article', name='article'),
    url(r"^articles/(?P<article_id>[0-9]+)/comments/$", 'blog.views.add_comment_article', name='add_comment_article'),
    url(r"^users/(?P<username>\w+)/$", 'blog.views.user_profile', name='user_profile'),
    url(r"^users/(?P<username>\w+)/comments/$", 'blog.views.user_comments', name='user_comments'),
    url(r"^users/(?P<username>\w+)/articles/$", 'blog.views.user_articles', name='user_articles'),
    url(r"^test/$", 'blog.views.test', name='test'),

]
