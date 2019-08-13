import time
import json
import requests
import os

USER_NUMBER = 5
API_CALL_SLEEP = 0.1

LOCALHOST_ENDPOINT = "http://127.0.0.1:8000/"
CREATE_USER_ENDPOINT = LOCALHOST_ENDPOINT + "api/user/usercreate"
LOGIN_USER_ENDPOINT = LOCALHOST_ENDPOINT + "api/user/userlogin"
DELETE_USER_ENDPOINT = LOCALHOST_ENDPOINT + "api/user/userdelete"


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


for id in userIdList:
    r = requests.get(url = DELETE_USER_ENDPOINT + '/' + id)
    if r.status_code != 200:
        print("############################################################")
        print(data)
        print(r)
        exit(-1)
    time.sleep(API_CALL_SLEEP)


