import base64
import hashlib
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from struct import unpack

from simdev.index.models import Record


def index(request):
    return HttpResponse('Simdev main page.')


def data_get(request):
    auth_hash = request.GET.get(u'hash', '').lower()
    if request.user.is_authenticated:
        if len(auth_hash) == 32 and request.user.username == auth_hash or len(auth_hash) == 0:
            return get_rating_for(request.user)
        else:
            logout(request)
    elif len(auth_hash) == 32:
        try:
            user = User.objects.get(username=auth_hash)
            login(request, user)
            return get_rating_for(user)
        except User.DoesNotExist:
            pass
    return get_rating_for(None)


def data_set(request):
    if request.user.is_authenticated:
        data = json.loads(request.GET.get(u'data', u'{}'))
        scores = decode(data.get(u'scores'))
        if scores > 0:
            del data[u'scores']
            try:
                record = request.user.record
            except Record.DoesNotExist:
                record = Record(user=request.user, scores=scores)
            record.scores = scores
            record.data = json.dumps(data)
            record.save()
        return HttpResponse('{"cmd": "login", "result": "success"}')
    return HttpResponse('{"error": "Not authenticated"}')


def decode(encoded):
    if encoded is None:
        return long(0)
    try:
        binary = base64.decodestring(encoded)
        scores_hash = binary[0:32]
        binary = binary[32:]
        length = unpack('>i', binary[0:4])[0]
        binary = binary[4:]
        scores = u''
        for i in xrange(len(binary) / 4):
            chunk = unpack('>I', binary[i * 4:(i + 1) * 4])[0] ^ 0xe6eeefe0
            for i in (24, 16, 8, 0):
                scores += unichr(chunk >> i & 0xff)
        scores = scores[0:length]
        m = hashlib.md5()
        m.update(scores.encode('utf-8'))
        if m.hexdigest() == scores_hash:
            return long(scores)
    except Exception as e:
        pass
    return long(0)


def auth(request):
    if request.GET.has_key(u'username') and request.GET.has_key(u'password'):
        username = request.GET[u'username'].strip()[:12]
        password = request.GET[u'password'][:50]
        if len(username) >= 3 and len(password) >= 4:
            m = hashlib.md5()
            m.update(username.encode('utf-8'))
            m.update(password.encode('utf-8'))
            auth_hash = m.hexdigest()
            if request.user.is_authenticated:
                if request.user.username == auth_hash:
                    return HttpResponse('{"cmd": "login", "result": "success"}')
                else:
                    logout(request)
                    return HttpResponse('{"error": "Wrong login password"}')
            else:
                user = authenticate(username=auth_hash, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponse('{"cmd": "login", "result": "success"}')
                else:
                    return HttpResponse('{"error": "Not registered"}')
    if request.user.is_authenticated:
        return HttpResponse('{"cmd": "login", "result": "success"}')
    return HttpResponse('{"error": "Wrong login password"}')


def register(request):
    if request.user.is_authenticated:
        logout(request)
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
