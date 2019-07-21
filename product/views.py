import json

from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.template import RequestContext
from django.template.context_processors import csrf

from product.models import User
from product.models import Transaction
from product.models import Connection
from product.models import Chat


def hello(request):
    return HttpResponse()

# /api/user/userlogin
def userLogin(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    username = body['username']
    password = body['password']

    result = User.objects.filter(userName=username,password=password)

    if result.count() == 1:
        return JsonResponse(result[0].json())
    else:
        return HttpResponse(status=403)


# /api/user/usercreate
def userCreate(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    user = User(userName=body['username'],
                firstName=body['firstname'],
                lastName=body['lastname'],
                password=body['password'],
                phone=body['phone'],
                email=body['email'])

    try:
        user.save()
    except IntegrityError or ValueError as err:
        return HttpResponse(status=400)

    return HttpResponse(status=200)

# /api/user/userupdate
def userUpdate(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    User.objects.filter(username=body['username']).update(
        firstName=body['firstname'],
        lastName=body['lastname'],
        password=body['password'],
        phone=body['phone'],
        email=body['email'],
    )

    return HttpResponse(status=200)

# /api/user/userdelete
def userDelete(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    User.objects.filter(username=body['username']).delete()

    return HttpResponse(status=200)

