from django.conf.urls import patterns, url

from .views import (register)

urlpatterns = patterns('',
    url(r'^user/register/$',
        register, name='register'),
)