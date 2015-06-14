from django.conf.urls import patterns, url

from .views import (courses, add_course, course_page, add_quiz)

urlpatterns = patterns('',
    url(r'^courses/add/$',
        add_course, name='add_course'),
    url(r'^courses/$',
        courses, name='courses'),
    url(r'^courses/(?P<course_id>\w+)/$',
        course_page, name='course_page'),
    url(r'^courses/(?P<course_id>\w+)/quizzes/add/$',
        add_quiz, name='add_quiz'),

)