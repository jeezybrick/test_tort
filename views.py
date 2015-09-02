import os.path
from django.core.files.storage import Storage
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.utils import timezone
from .forms import ContactForm, MyRegForm, AvatarForm, EditProfileForm, AddCommentForm
from PIL import Image
from blog.models import Article, Comments
from .my_func import check_if_avatar_exists
# from django.http import Http404


# Create your views here.
def home(request):
    link_to_avatar = check_if_avatar_exists(request)
    context = {
        'link_to_avatar': link_to_avatar,
    }
    return render(request, 'blog/home.html', context)


def about(request):
    link_to_avatar = check_if_avatar_exists(request)
    return render(request, 'blog/about.html', {'link_to_avatar': link_to_avatar})


def contact(request):
    link_to_avatar = check_if_avatar_exists(request)
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        subject = 'Моя тема'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'другой имеил']
        contact_message = "%s: %s via %s" % (
            form_full_name,
            form_message,
            form_email)
        send_mail(subject,
                  contact_message,
                  from_email,
                  [to_email],
                  fail_silently=False
                  )
        print(form.cleaned_data)
    context = {
        'form': form,
        'link_to_avatar': link_to_avatar
    }
    return render(request, 'blog/contact.html', context)


def news(request):
    link_to_avatar = check_if_avatar_exists(request)
    time = timezone.now
    articles_list = Article.objects.order_by('-id')
    paginator = Paginator(articles_list, 3)  # Show 3 contacts per page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        # raise Http404("Новости с таким адресом не существует")
        articles = paginator.page(paginator.num_pages)
    context = {
        'articles': articles,
        'link_to_avatar': link_to_avatar,
        'time': time,
    }
    return render(request, 'blog/news.html', context)


def show_article(request, article_id):
    link_to_avatar = check_if_avatar_exists(request)
    article = get_object_or_404(Article, id=article_id)
    comments = article.comments_set.all()
    form = AddCommentForm()
    return render(request, 'blog/article.html', {'article': article,
                                                 'comments': comments,
                                                 'link_to_avatar': link_to_avatar,
                                                 'form': form,
                                                 })


def my_show(request):
    link_to_avatar = check_if_avatar_exists(request)
    return render(request, 'blog/my.html', {'link_to_avatar': link_to_avatar})


def my_news(request):
    # articles = Article.objects.filter(user_id=request.user.id)
    articles = request.user.article_set.order_by('-id')
    link_to_avatar = check_if_avatar_exists(request)
    return render(request, 'blog/my_news.html', {'link_to_avatar': link_to_avatar, 'articles': articles})


def my_edit(request):
    # link_to_avatar = check_if_avatar_exists(request)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'blog/my_edit.html', {'form': form, 'link_to_avatar': link_to_avatar})


def my_edit_avatar(request):
    link_to_avatar = check_if_avatar_exists(request)
    avatar_exist = os.path.isfile("blog/static/blog/img/avatars/" + str(request.user.id) + '.jpg')
    if avatar_exist:
        avatar_size = os.path.getsize("blog/static/blog/img/avatars/" + str(request.user.id) + '.jpg')
    else:
        avatar_size = False
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            ext = request.FILES['avatar'].name[-4:]

            def handle_uploaded_file(f):
                with open("blog/static/blog/img/avatars/" + str(request.user.id) + ext, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                        try:
                            request.POST['bl_wh']
                        except Exception as e:
                            print(e)
                        else:
                            meme = Image.open(destination)
                            blc_wht = meme.convert("L")
                            blc_wht.save("blog/static/blog/img/avatars/" + str(request.user.id) + ext)
                        '''
                        width, height = meme.size
                        area = (int(width/4), int(height/4), int(3 * width/4), int(3 * height/4))
                        cropped_image = meme.crop(area)
                        cropped_image.save("blog/static/blog/img/avatars/" + str(request.user.id) + ext)
                        '''
            handle_uploaded_file(request.FILES['avatar'])
            return HttpResponseRedirect('/my/edit/avatar/success/')
    else:
        form = AvatarForm()
    return render(request, 'blog/edit_avatar.html', {'form': form,
                                                     'avatar_exist': avatar_exist,
                                                     'avatar_size': avatar_size,
                                                     'link_to_avatar': link_to_avatar,
                                                     })


def my_edit_avatar_success(request):
    return render(request, 'blog/edit_avatar_success.html')


def my_delete(request):
    # if request.method == 'DELETE':
    request.user.delete()
    return HttpResponseRedirect('/')


def get_login(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'blog/login.html', c)


def post_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/auth/success')
        else:
            return HttpResponseRedirect('/auth/disabled')

    else:
        return HttpResponseRedirect('/auth/fail')


def get_register(request):
    if request.method == 'POST':
        form = MyRegForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/auth/register/success')
    else:
        form = MyRegForm()

    return render(request, 'blog/register.html', {'form': form})


def register_success(request):
    link_to_avatar = check_if_avatar_exists(request)
    return render(request, 'blog/register_success.html', {'link_to_avatar': link_to_avatar})


def get_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_success(request):
    link_to_avatar = check_if_avatar_exists(request)
    return render(request, 'blog/login_success.html', {'link_to_avatar': link_to_avatar})


def add_comment_article(request, article_id):
    form = AddCommentForm(request.POST)
    if form.is_valid():
        article = get_object_or_404(Article, id=article_id)
        first = form.save(commit=False)
        first.user = request.user
        first.news = article
        first.save()
        return HttpResponseRedirect('/articles/'+article_id+'/')
    return HttpResponseRedirect('/articles/'+article_id+'/')


def user_profile(request, username):
    link_to_avatar = check_if_avatar_exists(request)
    user = get_object_or_404(User, username=username)
    return render(request, 'blog/user_profile.html', {'user': user,
                                                      'link_to_avatar': link_to_avatar,
                                                      })


def user_articles(request, username):
    link_to_avatar = check_if_avatar_exists(request)
    user = get_object_or_404(User, username=username)
    articles = user.article_set.all()
    return render(request, 'blog/user_articles.html', {'user': user,
                                                       'link_to_avatar': link_to_avatar,
                                                       'articles': articles,
                                                       })


def user_comments(request, username):
    link_to_avatar = check_if_avatar_exists(request)
    user = get_object_or_404(User, username=username)
    comments = user.comments_set.all()
    return render(request, 'blog/user_comments.html', {'user': user,
                                                       'link_to_avatar': link_to_avatar,
                                                       'comments': comments,
                                                       })


def test(request):
    if not request.user.is_staff:
        return HttpResponseRedirect('/')
    link_to_avatar = check_if_avatar_exists(request)
    form = None
    info = None
    none_var = None
    time = timezone.now
    if request.method == 'GET':
        form = AddCommentForm()
        info = dict(request.GET)
    elif request.method == 'POST':
        form = AddCommentForm(request.POST)
        info = request.POST
        messages.error(request, 'Ошибка!.', extra_tags='danger')
        messages.success(request, 'Все норм!.')
        none_var = False
    return render(request, 'blog/test.html', {'link_to_avatar': link_to_avatar,
                                              'form': form,
                                              'info': info,
                                              'none_var': none_var})