from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    userName = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)

    def json(self):
        result = {'firstname': self.firstName,
                  'lastname': self.lastName,
                  'email': self.email,
                  'phone': self.phone.__str__(),
                  'username': self.userName}
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


class Connection(models.Model):
    fromUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connectionFromUser')
    toUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connectionToUser')
    CONNECTION_STATUS = {
        (0, 'REQUEST'),
        (1, 'ACCEPT'),
        (2, 'BLOCK'),
    }
    status = models.IntegerField(choices=CONNECTION_STATUS, default=0)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)


class Chat(models.Model):
    title = models.CharField(max_length=30)
    listUser = models.ManyToManyField(
        User,
    )
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
