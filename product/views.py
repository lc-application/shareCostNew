import json

from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.template import RequestContext
from django.template.context_processors import csrf
from django.core import files

from product.models import BaseUser
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

    result = User.objects.filter(base__userName=username,password=password)

    if result.count() == 1:
        return JsonResponse(result[0].json())
    else:
        return HttpResponse(status=403)


# /api/user/usercreate
def userCreate(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    base = BaseUser(userName=body['username'],
                    firstName=body['firstname'],
                    lastName=body['lastname'],
                    image=request.FILES)
    user = User(base=base,
                password=body['password'],
                phone=body['phone'],
                email=body['email']
                )

    try:
        base.save()
        user.save()
    except IntegrityError or ValueError as err:
        return HttpResponse(status=400)

    return HttpResponse(status=200)

# /api/user/userupdate
def userUpdate(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    BaseUser.objects.filter(userName=body['username']).update(
        base__firstName=body['firstname'],
        base__lastName=body['lastname'],
        image=request.FILES
    )
    User.objects.filter(base__userName=body['username']).update(
        password=body['password'],
        phone=body['phone'],
        email=body['email'],
    )

    return HttpResponse(status=200)

# /api/user/userdelete
def userDelete(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    User.objects.filter(base__userName=body['username']).delete()
    BaseUser.objects.filter(userName=body['username'])

    return HttpResponse(status=200)

# /api/friend/request
def friendRequest(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    # From is a user id, to is a username.
    fromUser = User.objects.get(base__id=body['from'])
    toUser = User.objects.get(base__id=body['to'])

    connectionFrom = Connection(toUser=toUser.base, status=1)
    connectionTo = Connection(toUser=fromUser.base, status=0)
    connectionFrom.save()
    connectionTo.save()

    fromUser.listConnection.add(connectionFrom)
    toUser.listConnection.add(connectionTo)

    fromUser.save()
    toUser.save()

    return HttpResponse(status=200)

# /api/friend/confirm
def friendConfirm(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    fromUser = User.objects.get(base__id=body['from'])
    toUser = User.objects.get(base__id=body['to'])

    for connection in fromUser.listConnection.all():
        if connection.toUser.userName == toUser.base.userName:
            connection.status = 2
            break

    for connection in toUser.listConnection.all():
        if connection.toUser.userName == fromUser.base.userName:
            connection.status = 2
            break

    fromUser.save()
    toUser.save()

    return HttpResponse(status=200)


# /api/friend/delete
def friendDelete(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    fromUser = User.objects.get(base__id=body['from'])
    toUser = User.objects.get(base__id=body['to'])

    for connection in fromUser.listConnection.all():
        if connection.toUser.userName == toUser.base.userName:
            fromUser.listConnection.remove(connection)

    for connection in toUser.listConnection.all():
        if connection.toUser.userName == fromUser.base.userName:
            toUser.listConnection.remove(connection)

    fromUser.save()
    toUser.save()

    return HttpResponse(status=200)



# /api/friend/get
# status :(0, 'REQUEST'), (1, 'PENDING'), (2, 'ACCEPT'), (3, 'BLOCK'),
def friendGet(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    user = User.objects.get(base__id=body['from'])

    result = []
    for connection in user.listConnection.all():
        if str(connection.status) == body['status']:
            result.append(connection.toUser.json())

    return JsonResponse(result, safe=False)

# /api/connection/get
def allConnections(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    user = User.objects.get(base__id=body['identifier'])
    return JsonResponse(user.listConnection)

