import time
import json
import requests
from random import randrange

USER_NUMBER = 5
API_CALL_SLEEP = 0.1


LOCALHOST_ENDPOINT = "http://127.0.0.1:8000/"
CREATE_USER_ENDPOINT = LOCALHOST_ENDPOINT + "api/user/usercreate"
LOGIN_USER_ENDPOINT = LOCALHOST_ENDPOINT + "api/user/userlogin"
DELETE_USER_ENDPOINT = LOCALHOST_ENDPOINT + "api/user/userdelete"

RELATION_REQUEST = LOCALHOST_ENDPOINT + "api/friend/request"
RELATION_CONFIRM = LOCALHOST_ENDPOINT + "api/friend/confirm"
RELATION_DELETE  = LOCALHOST_ENDPOINT + "api/friend/delete"
def relation(user1, user2, relation):
    if relation == 2 or relation == 1:
        r = requests.get(RELATION_REQUEST + "/" + user1 + "/" + user2)
        if r.status_code != 200:
            print("############################################################")
            print(r)
            exit(-1)
        time.sleep(API_CALL_SLEEP)

        if relation == 1:
            r = requests.get(RELATION_CONFIRM + "/" + user2 + "/" + user1)
            if r.status_code != 200:
                print("############################################################")
                print(r)
                exit(-1)
            time.sleep(API_CALL_SLEEP)

userIdList = []

i = 0
while i < USER_NUMBER:
    ii = i.__str__()
    data = {
        'username' : 'username' + ii,
        'firstname' : 'firstname' + ii,
        'lastname' : 'lastname' + ii,
        'password' : 'password' + ii,
        'phone' : '+1857991' + ii.zfill(4),
        'email' : 'test' + ii + '@lol.com'
    }

    r = requests.post(url = CREATE_USER_ENDPOINT, data = json.dumps(data))

    if r.status_code != 200:
        print("############################################################")
        print(data)
        print(r)
        exit(-1)
    time.sleep(API_CALL_SLEEP)
    i += 1


i = 0
while i < USER_NUMBER:
    ii = i.__str__()
    data = {
        'username' : 'username' + ii,
        'password' : 'password' + ii
    }

    r = requests.post(url = LOGIN_USER_ENDPOINT, data = json.dumps(data))

    if r.status_code != 200:
        print("############################################################")
        print(data)
        print(r)
        exit(-1)
    userIdList.append(r.json()['id'])
    time.sleep(API_CALL_SLEEP)
    i += 1


userRelationMatrix = [[]] * USER_NUMBER
### 0 - no relation, 1 - friend, 2 - request 3-pending
### no block for now
RELATION_MAP = ["NO", "FRIEND", "REQUEST", "PENDING"]
x = 0
while x < USER_NUMBER:
    userRelationMatrix[x] = [0] * USER_NUMBER
    x+=1
x = 0
print("User Relation: From \ To \ Relation")
while x < USER_NUMBER:
    y = x + 1
    while y < USER_NUMBER:
        value = randrange(3)
        userRelationMatrix[x][y] = value
        print("from:" + x.__str__() + userIdList[x] + " to:" + y.__str__() + userIdList[y] +  " relation:" + RELATION_MAP[value])
        if value == 2:
            print("from:" + y.__str__() + userIdList[x] + " to:" + x.__str__() + userIdList[y] + " relation:" + RELATION_MAP[3])

        if value != 0:
            relation(userIdList[x], userIdList[y], value)
        y += 1
    x += 1


### may be manual cleanup is better for test

# for id in userIdList:
#      r = requests.get(url = DELETE_USER_ENDPOINT + '/' + id)
#      if r.status_code != 200:
#          print("############################################################")
#          print(data)
#          print(r)
#          exit(-1)
#      time.sleep(API_CALL_SLEEP)


