import os.path


def check_if_avatar_exists(request):
    avatar_exist = os.path.isfile("blog/static/blog/img/avatars/" + str(request.user.id) + '.jpg')
    if not avatar_exist:
        return 'blog/img/avatars/default.jpg'
    else:
        return 'blog/img/avatars/' + str(request.user.id) + '.jpg'
