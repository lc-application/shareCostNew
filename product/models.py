from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Connection(models.Model):
    toUser = models.CharField(max_length=30)
    CONNECTION_STATUS = {
        (0, 'REQUEST'),
        (1, 'PENDING'),
        (2, 'ACCEPT'),
        (3, 'BLOCK'),
    }
    status = models.IntegerField(choices=CONNECTION_STATUS, default=0)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)


class User(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    userName = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    listConnection = models.ManyToManyField(
        Connection,
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to="UserImage",blank=True)

    def json(self):
        result = {'firstname': self.firstName,
                  'lastname': self.lastName,
                  'email': self.email,
                  'phone': self.phone.__str__(),
                  'username': self.userName,
                  'image':self.image.path}
        return result


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
