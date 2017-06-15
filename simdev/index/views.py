from django.http import HttpResponse


def index(request):
    return HttpResponse('Simdev main page.')


def data_get(request):
    return HttpResponse('{"error": "unregistered"}')


def data_set(request):
    return HttpResponse('{"error": "unregistered"}')

