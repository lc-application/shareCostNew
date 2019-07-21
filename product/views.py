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

# /api/friend/request
def friendRequest(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    fromUser = User.objects.get(username=body['from'])
    toUser = User.objects.get(username=body['to'])

    connectionFrom = Connection(toUser=toUser.userName, status=1)
    connectionTo = Connection(toUser=fromUser.userName, status=0)

    fromUser.listConnection.add(connectionFrom)
    toUser.listConnection.add(connectionTo)

    fromUser.save()
    toUser.save()

    return HttpResponse(status=200)

# /api/friend/confirm
def friendConfirm(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    fromUser = User.objects.get(username=body['from'])
    toUser = User.objects.get(username=body['to'])

    for connection in fromUser.listConnection:
        if(connection.toUser == toUser.userName):
            connection.status = 2
            break

    for connection in toUser.listConnection:
        if(connection.toUser == fromUser.userName):
            connection.status = 2
            break

    fromUser.save()
    toUser.save()

    return HttpResponse(status=200)


# /api/friend/delete
def friendIgnore(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    fromUser = User.objects.get(username=body['from'])
    toUser = User.objects.get(username=body['to'])

    for connection in fromUser.listConnection:
        if(connection.toUser == toUser.userName):
            fromUser.listConnection.remove(connection)

    for connection in toUser.listConnection:
        if(connection.toUser == fromUser.userName):
            toUser.listConnection.remove(connection)

    fromUser.save()
    toUser.save()

    return HttpResponse(status=200)



# /api/friend/get
# status :(0, 'REQUEST'), (1, 'PENDING'), (2, 'ACCEPT'), (3, 'BLOCK'),
def friendGet(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    user = User.objects.get(username=body['from'])

    result = []
    for connection in user.listConnection:
        if(connection.status == body['status']):
            result.append(User.objects.get(connection.toUser).json())

    return JsonResponse(result)

