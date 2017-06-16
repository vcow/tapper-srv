import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse


def index(request):
    return HttpResponse('Simdev main page.')


def data_get(request):
    if request.user.is_authenticated:
        return get_rating_for(request.user)
    elif request.GET.has_key(u'hash'):
        auth_hash = request.GET[u'hash']
        if len(auth_hash) == 32:
            user = User.objects.get(first_name=auth_hash)
            if user is not None:
                user = authenticate(request, username=user.username, password=user.password)
                login(request, user)
                return get_rating_for(user)
    return get_rating_for(None)


def data_set(request):
    if request.GET.has_key(u'user') and request.GET.has_key(u'password'):
        username = str(request.GET[u'user']).strip()[:12]
        password = str(request.GET[u'password']).strip()[:50]
        if len(username) >= 3 and len(password) >= 4:
            user = authenticate(request, username=username, password=password)
    return HttpResponse('{"error": "unregistered"}')


def get_rating_for(user):
    leaders = User.objects.filter(record__isnull=False).order_by('record__scores')[:10]
    return HttpResponse('{}')
