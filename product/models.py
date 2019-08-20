import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class BaseUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    userName = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to="UserImage",blank=True)

    def json(self):
        result = {'id': self.id,
                'firstname': self.firstName,
                'lastname': self.lastName,
                'username': self.userName
                ##'image':self.image.path
        }
        return result

    def __str__(self):
        return 'Base User: ' + self.firstName


class Transaction(models.Model):
    fromUser = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING, related_name='transactionFromUser')
    toUser = models.ForeignKey(BaseUser, on_delete=models.DO_NOTHING, related_name='transactionToUser')
    value = models.FloatField()
    title = models.CharField(max_length=30)
    comment = models.CharField(max_length=200)
    TRANSACTION_STATUS = (
        (0, 'CREATE'),
        (1, 'ACCEPT'),
        (2, 'DENY'),
        (3, 'FINISH'),
    )
    status = models.IntegerField(choices=TRANSACTION_STATUS, default=0)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def json(self):
        result = {'from':self.fromUser,
                  'to':self.toUser,
                  'value':self.value,
                  'title':self.title,
                  'comment':self.comment,
                  'status':self.status,
                  'create':self.createDate,
                  'update':self.updateDate}
        return result


class Chat(models.Model):
    title = models.CharField(max_length=30)
    listUser = models.ManyToManyField(
        BaseUser
    )
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)


class Event(models.Model):
    title = models.CharField(max_length=30)
    summary = models.CharField(max_length=200)
    hostUser = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='host')
    startTime = models.DateTimeField()
    endTime = models.DateField()
    listUser = models.ManyToManyField(
        BaseUser
    )
    image = models.ImageField(upload_to="EventImage", blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    category= models.CharField(max_length=30)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def json(self):
        result = {
            'title':self.title,
            'summary':self.summary,
            'hostUser':self.hostUser.json(),
            'startTime':self.startTime,
            'endTime':self.endTime,
            'listUser':self.listUser
            # 'image':self.image.path
        }
        return result

    def header(self):
        return {
            'title':self.title,
            'category':self.category,
            'summary': self.summary,
            'id': self.id
        }
    
    def __str__(self):
        return 'Event: ' + self.title


class User(models.Model):
    base = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True, unique=True)
    password = models.CharField(max_length=30)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    listFriend = models.ManyToManyField('self')
    listBlock = models.ManyToManyField('self')
    listRequest = models.ManyToManyField('self')
    listPendRequest = models.ManyToManyField('self')

    def __str__(self):
        return 'User: ' + self.base.firstName

    def baseJson(self):
        return self.base.json()

    def listUserToJson(self, list):
        result = []
        for user in list:
            result.append(user.baseJson())
        return result

    def json(self):
        result = self.baseJson()
        result['email'] = self.email
        result['phone'] = self.phone.__str__()
        result['listFriend'] = self.listUserToJson(self.listFriend.all())
        result['listBlock'] = self.listUserToJson(self.listBlock.all())
        result['listRequest'] = self.listUserToJson(self.listRequest.all())
        result['listPendRequest'] = self.listUserToJson(self.listPendRequest.all())
        return result
