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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from product.views import hello
from shareCost import settings

from product.views import userLogin
from product.views import userCreate
from product.views import userUpdate
from product.views import userDelete

from product.views import friendRequest
from product.views import friendConfirm
from product.views import friendDelete


from product.views import relationGetFriend
from product.views import relationGetPending
from product.views import relationGetRequest
urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello),
    path('api/user/userlogin', userLogin),
    path('api/user/usercreate', userCreate),
    path('api/user/userupdate', userUpdate),
    path('api/user/userdelete/<userid>', userDelete),
    path('api/friend/request/<userfrom>/<userto>', friendRequest),
    path('api/friend/confirm/<userfrom>/<userto>', friendConfirm),
    path('api/friend/delete/<userfrom>/<userto>', friendDelete),
    path('api/friend/getfriend/<userid>', relationGetFriend),
    path('api/friend/getpending/<userid>', relationGetPending),
    path('api/friend/getrequest/<userid>', relationGetRequest),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)