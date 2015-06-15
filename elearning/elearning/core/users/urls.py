from django.conf.urls import patterns, url

from .views import (register, login)

urlpatterns = patterns('',
    url(r'^user/register/$',
        register, name='register'),
                       url(r'^user/login/$',
                           login, name='login'),
)
