from django.contrib import admin

# Register your models here.
from product.models import User
from product.models import Transaction
from product.models import Connection
from product.models import Chat

admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Connection)
admin.site.register(Chat)