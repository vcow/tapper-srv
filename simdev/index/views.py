import hashlib
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse

from simdev.index.models import Record


def index(request):
    return HttpResponse('Simdev main page.')


def data_get(request):
    auth_hash = request.GET.get(u'hash', '').lower()
    if request.user.is_authenticated:
        if len(auth_hash) == 32 and request.user.username == auth_hash or len(auth_hash) == 0:
            return get_rating_for(request.user)
    elif len(auth_hash) == 32:
        try:
            user = User.objects.get(username=auth_hash)
            login(request, user)
            return get_rating_for(user)
        except User.DoesNotExist:
            pass
    return get_rating_for(None)


def data_set(request):
    auth_hash = request.GET.get(u'hash', '').lower()
    if request.user.is_authenticated:
        if request.user.username != auth_hash:
            return HttpResponse('{"error": "Wrong hash"}')
        else:
            user = request.user
    else:
        try:
            user = User.objects.get(username=auth_hash)
            login(request, user)
        except User.DoesNotExist:
            return HttpResponse('{"error": "Not registered"}')
    scores = long(request.GET.get(u'scores', '0'))
    if scores > 0:
        try:
            user.record.scores = scores
            user.record.save()
        except Record.DoesNotExist:
            record = Record(user=user, scores=scores)
            record.save()
    return get_rating_for(user)


def auth(request):
    if request.user.is_authenticated:
        return HttpResponse('{"cmd": "login", "result": "success"}')
    if request.GET.has_key(u'username') and request.GET.has_key(u'password'):
        username = request.GET[u'username'].strip()[:12]
        password = request.GET[u'password'][:50]
        if len(username) >= 3 and len(password) >= 4:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('{"cmd": "login", "result": "success"}')
            else:
                return HttpResponse('{"error": "Not registered"}')
    return HttpResponse('{"error": "Wrong login password"}')


def register(request):
    if request.GET.has_key(u'username') and request.GET.has_key(u'password'):
        username = request.GET[u'username'].strip()[:12]
        password = request.GET[u'password'][:50]
        if len(username) >= 3 and len(password) >= 4:
            m = hashlib.md5()
            m.update(username.encode('utf-8'))
            m.update(password.encode('utf-8'))
            auth_hash = m.hexdigest()
            try:
                user = User.objects.get(username=auth_hash)
                return HttpResponse({'error': 'Already registered'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=auth_hash, password=password, first_name=username)
                return HttpResponse('{"cmd": "register", "result": "success"}')
    return HttpResponse('{"error": "Wrong login password"}')


def get_rating_for(user):
    leaders = User.objects.filter(record__isnull=False).order_by('record__scores')[:10]
    return HttpResponse('{}')
