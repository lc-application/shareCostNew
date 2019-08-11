import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class User(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    userName = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="UserImage",blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def friendJson(self):
        return {'id': self.id, 'firstname': self.firstName, 'lastname': self.lastName, 'username': self.userName}

    def json(self):
        connections = []
        all_connections = self.received_connections.all() | self.sent_connections.all()
        for connection in all_connections:
            userJson = connection.toUser.friendJson()
            connections.append({"user":userJson, "status":str(connection.status)})
        result = {'firstname': self.firstName,
                  'lastname': self.lastName,
                  'email': self.email,
                  'phone': self.phone.__str__(),
                  'username': self.userName,
                  'id': self.id,
                  'listConnection': connections}
        # if bool(self.image):
        #     result['image'] = self.image.path
        return result

    def __str__(self):
        return 'User: ' + self.firstName

class Connection(models.Model):
    toUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_connections")
    fromUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_connections")
    CONNECTION_STATUS = {
        (0, 'PENDING'),
        (1, 'ACCEPT'),
        (2, 'BLOCK'),
    }
    status = models.IntegerField(choices=CONNECTION_STATUS, default=0)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return 'Connection from: ' + self.fromUser.firstName + '. to: ' + self.toUser.firstName + '. Status: ' + str(self.get_status_display())

class Transaction(models.Model):
    fromUser = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='transactionFromUser')
    toUser = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='transactionToUser')
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
        User,
    )
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)


class Event(models.Model):
    title = models.CharField(max_length=30)
    summary = models.CharField(max_length=200)
    hostUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host')
    startTime = models.DateTimeField()
    endTime = models.DateField()
    listUser = models.ManyToManyField(
        User
    )
    image = models.ImageField(upload_to="EventImage")
    createDate = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    def json(self):
        result = {
            'title':self.title,
            'summary':self.summary,
            'hostUser':self.hostUser.json(),
            'startTime':self.startTime,
            'endTime':self.endTime,
            'listUser':self.listUser,
            'image':self.image.path
        }
        return result
