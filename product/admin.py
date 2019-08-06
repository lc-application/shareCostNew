from django.contrib import admin

# Register your models here.

from product.models import BaseUser
from product.models import Connection
from product.models import Transaction
from product.models import Chat
from product.models import Event
from product.models import User

admin.site.register(BaseUser)
admin.site.register(Connection)
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Chat)
admin.site.register(Event)