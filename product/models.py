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


class Connection(models.Model):
    toUser = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="received_connections")
    fromUser = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="sent_connections")
    CONNECTION_STATUS = {
        (0, 'PENDING'),
        (1, 'ACCEPT'),
        (2, 'BLOCK'),
    }
    status = models.IntegerField(choices=CONNECTION_STATUS, default=0)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def json(self):
        result = {
            'from':self.fromUser.json(),
            'to':self.toUser.json(),
            'status': self.status.__str__(),
        }
        return result

    def __str__(self):
        return 'Connection from: ' + self.fromUser.firstName + '. to: ' + self.toUser.firstName + '. Status: ' + str(self.get_status_display())


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


class User(models.Model):
    base = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True, unique=True)
    password = models.CharField(max_length=30)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    listEvent = models.ManyToManyField(
        Event,
        blank=True,
    )

    def baseJson(self):
        return self.base.json()

    def json(self):
        connections = []
        all_connections = self.received_connections.all() | self.sent_connections.all()
        for connection in all_connections:
            connections.append(connection.json())

        result = self.baseJson()
        result['email'] = self.email
        result['phone'] = self.phone.__str__()
        result['listConnection'] = connections
        return result

    def __str__(self):
        return 'User: ' + self.base.userName
