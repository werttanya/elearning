import requests
import urlparse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from collections import namedtuple
from django.shortcuts import redirect, render
from elearning.settings import REST_API
from django.http import HttpResponseBadRequest, HttpResponse
from django.core.urlresolvers import reverse
from .forms import CourseForm
import logging
import json
from datetime import datetime

logger = logging.getLogger()
def json_object_hook(response):
    """
    Convert JSON representation of response to object one.

    :param response: :class:`HTTPResponse` object
    :returns: :class:`JSONResponse` object
    """
    return namedtuple('JSONResponse', response.keys())(*response.values())

def get_page_from_request(request, key='page'):
    """
    Get current page number from the request

    :param request: :class:`Request` object
    :param key: Optional key to extract from the query string instead of page
    :type key: str
    :returns: Page number
    """
    params = dict(urlparse.parse_qsl(request.META['QUERY_STRING']))
    page = params.pop(key, 1)
    return page

def courses(request):
    page = get_page_from_request(request)
    url='/account/authored'
    accept_json_header = {'accept': 'application/json'}
    email = request.session['email']
    password = request.session['password']
    r = requests.get(REST_API+url, headers=accept_json_header, auth=(email, password))
    courses = r.json(object_hook=json_object_hook)
    paginator = Paginator(courses, 4)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    return render(request, 'courses/courses.html', {
        'courses': courses, 'paginator': paginator
    })


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        logger.warning(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            email = request.session['email']
            password = request.session['password']
            params = {'title': title, 'description': description}

            url = '/courses'
            r = requests.post(REST_API+url, data=params, auth=(email, password))
            if r.status_code == requests.codes.ok:
                courses_url = '/courses/'
                return redirect(courses_url)
            else:
                return HttpResponseBadRequest()
    form = CourseForm()
    return render(request, 'courses/add_course.html', {'form': form,})

def course_page(request, course_id):
    url='/courses/{0}'.format(course_id)
    accept_json_header = {'accept': 'application/json'}
    email = request.session['email']
    password = request.session['password']
    r = requests.get(REST_API+url, headers=accept_json_header, auth=(email, password))
    course = r.json(object_hook=json_object_hook)
    quizzes_url = '/quizzes?course_id={0}'.format(course_id)
    qr = requests.get(REST_API+quizzes_url, headers=accept_json_header, auth=(email, password))
    quizzes = qr.json(object_hook=json_object_hook)
    quizzes_dates = []
    for quiz in quizzes:
        if quiz.date_published:
            print quiz.date_published
            new_quiz = {}
            new_quiz['id'] = quiz.id
            new_quiz['datetime'] = datetime.strptime( quiz.date_published[:-4], "%Y-%m-%dT%H:%M:%S." ).strftime('%Y-%m-%d %H:%M:%S')
            quizzes_dates.append(new_quiz)
    return render(request, 'courses/course.html',
                  {'course': course,'quizzes': quizzes, 'dates':quizzes_dates})

def add_quiz(request, course_id):
    email = request.session['email']
    password = request.session['password']
    if request.method == 'POST':
        question_num = request.POST["numberOfQuestions"]
        title = request.POST["title"]
        description = request.POST["description"]
        questions = []
        url = '/quizzes'
        for i in range(int(question_num)):
            question = request.POST['question{0}'.format(i+1)]
            answers = [value for key, value in request.POST.iteritems()
                       if (key.lower().startswith('question{0}answer'.format(i+1))
                           and key != 'question{0}AnswersTrue'.format(i+1))]
            correctAnswerIndex = int(request.POST['question{0}AnswersTrue'.format(i+1)])-1
            questions.append({"question":question, "choices":answers, "correct":correctAnswerIndex})
        quiz = {"title": title, "description": description, "course_id": course_id, "questions": questions}
        r = requests.post(REST_API+url, data=json.dumps(quiz), headers={'content-type': 'application/json'},
                          auth=(email, password))
        if r.status_code == requests.codes.created:
            return redirect(reverse('course_page', args=[course_id]))
        else:
            return HttpResponseBadRequest()
    return render(request, 'courses/add_quiz.html')

def publish_quiz(request, course_id, quiz_id):
    print "insight"
    email = request.session['email']
    password = request.session['password']
    url ='/quizzes/{0}/publish'.format(quiz_id)
    if request.method == 'POST':
        text = request.POST["text"]
        r = requests.post(REST_API + url, data={'message': text}, auth=(email, password))
        if r.status_code == requests.codes.ok:
            json_data = json.dumps({"response":"ok","quiz_id":quiz_id})
        else:
            json_data = json.dumps({"response":"failed","quiz_id":quiz_id})
    r = HttpResponse(json_data, content_type = "application/json")
    print "insight2"
    return r

