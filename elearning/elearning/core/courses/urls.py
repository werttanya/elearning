from django.conf.urls import patterns, url

from .views import (courses, add_course, course_page, add_quiz, publish_quiz, quiz_page, close_quiz,
                    quiz_statistics, questions_statistics, motivation_statistics)
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
    url(r'^courses/(?P<course_id>\w+)/quizzes/(?P<quiz_id>\w+)/publish/$',
        publish_quiz, name='publish_quiz'),
    url(r'^courses/(?P<course_id>\w+)/quizzes/(?P<quiz_id>\w+)/close/$',
        close_quiz, name='close_quiz'),
    url(r'^courses/(?P<course_id>\w+)/quizzes/(?P<quiz_id>\w+)/$',
        user_login_required(quiz_page), name='quiz_page'),
    url(r'^quizzes/(?P<quiz_id>\w+)/statistic/$',
        quiz_statistics, name='quiz_statistics'),
    url(r'^quizzes/(?P<quiz_id>\w+)/statistic/questions/$',
        questions_statistics, name='questions_statistics'),
    url(r'^quizzes/(?P<quiz_id>\w+)/statistic/motivation/$',
        motivation_statistics, name='motivation_statistics'),
)