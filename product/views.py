import json

from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.template import RequestContext
from django.template.context_processors import csrf
from django.core import files
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from product.models import BaseUser
from product.models import User
from product.models import Transaction
from product.models import Chat
from product.models import Event


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
                    lastName=body['lastname'])
                    #image=request.FILES)
    user = User(base=base,
                password=body['password'],
                phone=body['phone'],
                email=body['email']
                )

    try:
        base.save()
        user.save()
    except IntegrityError or ValueError as err:
        print(err)
        base.delete()
        user.delete()
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
def userDelete(request, userid):

    BaseUser.objects.filter(id=userid).delete()
    return HttpResponse(status=200)

# /api/user/search

def userSearch(request, input):
    choices = BaseUser.objects.values_list('userName')
    filterChoices = process.extract(input, choices, limit=20)
    result = []
    for choice in filterChoices:
        result.append(BaseUser.objects.get(userName=choice[0][0]).json())
    return HttpResponse(result, status=200)



# /api/friend/request
def friendRequest(request, userfrom, userto):
    fromUser = User.objects.get(base__id=userfrom)
    toUser = User.objects.get(base__id=userto)

    try:
        fromUser.listRequest.add(toUser)
        fromUser.save()
        toUser.listPendRequest.add(fromUser)
        toUser.save()
    except:
        return HttpResponse(status=400)

    return HttpResponse(status=200)

# /api/friend/confirm
def friendConfirm(request, userfrom, userto):

    fromUser = User.objects.get(base__id=userfrom)
    toUser = User.objects.get(base__id=userto)

    try:
        fromUser.listPendRequest.remove(toUser)
        fromUser.listFriend.add(toUser)

        toUser.listRequest.remove(fromUser)
        toUser.listFriend.add(fromUser)

        fromUser.save()
        toUser.save()
    except:
        return HttpResponse(status=400)

    return HttpResponse(status=200)


# /api/friend/delete
def friendDelete(request, userfrom, userto):
    fromUser = User.objects.get(base__id=userfrom)
    toUser = User.objects.get(base__id=userto)

    try:
        fromUser.listFriend.remove(toUser)
        toUser.listFriend.remove(fromUser)
    except:
        return HttpResponse(status=400)
    return HttpResponse(status=200)



# /api/friend/getfriend
def relationGetFriend(request, userid):

    user = User.objects.get(base__id=userid)
    return JsonResponse(User.listUserToJson(user, user.listFriend.all()), safe=False)

# /api/friend/getPending
def relationGetPending(request, userid):

    user = User.objects.get(base__id=userid)
    return JsonResponse(User.listUserToJson(user, user.listPendRequest.all()), safe=False)



# /api/friend/getRequest
def relationGetRequest(request, userid):
    user = User.objects.get(base__id=userid)
    return JsonResponse(User.listUserToJson(user, user.listRequest.all()), safe=False)

# /api/event/allEvents
def allEvents(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    user = User.objects.get(base__id=body['user_id'])
    result = []
    for event in user.base.event_set.all():
        result.append(event.header())
    return JsonResponse(result, safe=False)

# /api/event/joinEvent
def joinEvent(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    event = Event.objects.get(base__id=body['event_id'])
    user = User.objects.get(base__id=body['user_id'])
    event.listUser.add(user)
    return HttpResponse(status=200)


# /api/event/eventDetail
def eventDetail(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    event = Event.objects.get(base__id=body['event_id'])

    return JsonResponse(event.json())


# /api/event/removeFromEvent
def removeFromEvent(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    event = Event.objects.get(base__id=body['event_id'])
    user = User.objects.get(base__id=body['user_id'])
    if user in event.listUser.all():
        event.listUser.delete(user)
    return HttpResponse(status=200)

  