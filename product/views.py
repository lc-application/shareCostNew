from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from product.models import User
from product.models import Transaction
from product.models import Connection
from product.models import Chat


def hello(request):
    return HttpResponse()
