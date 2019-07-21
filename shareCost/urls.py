"""shareCost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from product.views import hello

from product.views import userLogin
from product.views import userCreate
from product.views import userUpdate
from product.views import userDelete

from product.views import friendRequest
from product.views import friendConfirm
from product.views import friendDelete
from product.views import friendGet
urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello),
    path('api/user/userlogin', userLogin),
    path('api/user/usercreate', userCreate),
    path('api/user/userupdate', userUpdate),
    path('api/user/userdelete', userDelete),
    path('api/friend/request', friendRequest),
    path('api/friend/confirm', friendConfirm),
    path('api/friend/delete', friendDelete),
    path('api/friend/get', friendGet)
]
