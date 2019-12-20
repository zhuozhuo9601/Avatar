from django.shortcuts import redirect
from django.urls import reverse


def user_login(func):
    def warpper(request, *args, **kwargs):
        if request.COOKIES.get('username', False) and request.COOKIES.get('sessionid', False):
            return func(request, *args, **kwargs)
        else:
            return redirect(reverse('texts:login'))

    return warpper