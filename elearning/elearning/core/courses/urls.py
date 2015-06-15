from django.conf.urls import patterns, url

from .views import (courses, add_course, course_page, add_quiz)
from elearning.core.users.views import user_login_required

urlpatterns = patterns('',
    url(r'^courses/add/$',
        user_login_required(add_course), name='add_course'),
    url(r'^courses/$',
        user_login_required(courses), name='courses'),
    url(r'^courses/(?P<course_id>\w+)/$',
        user_login_required(course_page), name='course_page'),
    url(r'^courses/(?P<course_id>\w+)/quizzes/add/$',
        user_login_required(add_quiz), name='add_quiz'),

)