from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from collections import namedtuple
from django.shortcuts import redirect, render
from elearning.settings import REST_API, PYGAL_JS_FILES
from django.http import HttpResponseBadRequest, HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from elearning.core.errors.views import server_error
from .forms import CourseForm
from datetime import datetime
from pygal.style import Style
from pygal.colors import darken
from pygal.config import Config
import json
import pygal
import requests
import urlparse
import tempfile

custom_style = Style(
    background=darken('#f8f8f8', 3),
    plot_background='#f8f8f8',
    foreground='rgba(0, 0, 0, 0.9)',
    foreground_light='rgba(0, 0, 0, 0.9)',
    foreground_dark='rgba(0, 0, 0, 0.6)',
    opacity='.5',
    opacity_hover='.9',
    transition='250ms ease-in',
    colors=('#0ACF00','#0E51A7', '#FD0006', '#FF9E00'))

question_style = Style(
    background=darken('#f8f8f8', 3),
    plot_background='#f8f8f8',
    foreground='rgba(0, 0, 0, 0.9)',
    foreground_light='rgba(0, 0, 0, 0.9)',
    foreground_dark='rgba(0, 0, 0, 0.6)',
    opacity='.5',
    opacity_hover='.9',
    transition='250ms ease-in',
    colors = ('#0ACF00','#0E51A7', '#FD0006', '#FF9E00'))

motivation_style = Style(
    background=darken('#f8f8f8', 3),
    plot_background='#f8f8f8',
    foreground='rgba(0, 0, 0, 0.9)',
    foreground_light='rgba(0, 0, 0, 0.9)',
    foreground_dark='rgba(0, 0, 0, 0.6)',
    opacity='.5',
    opacity_hover='.9',
    transition='250ms ease-in',
    colors = ('#B6E354', '#FEED6C', '#FF5995'))

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
    if r.status_code == requests.codes.ok:
        courses = r.json(object_hook=json_object_hook)
    else:
        courses = []
        return server_error(request)
    paginator = Paginator(courses, 4)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    return render(request, 'courses/courses.html', {
        'courses': courses, 'paginator': paginator })


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
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
                return server_error(request)
    form = CourseForm()
    return render(request, 'courses/add_course.html', {'form': form,})

def course_page(request, course_id):
    url='/courses/{0}'.format(course_id)
    accept_json_header = {'accept': 'application/json'}
    email = request.session['email']
    password = request.session['password']
    r = requests.get(REST_API+url, headers=accept_json_header, auth=(email, password))
    if r.status_code != requests.codes.ok:
        return server_error(request)
    course = r.json(object_hook=json_object_hook)
    quizzes_url = '/quizzes?course_id={0}'.format(course_id)
    qr = requests.get(REST_API+quizzes_url, headers=accept_json_header, auth=(email, password))
    if qr.status_code != requests.codes.ok:
        return server_error(request)
    quizzes = qr.json(object_hook=json_object_hook)
    quizzes_dates = []
    for quiz in quizzes:
        if quiz.date_published:
            print quiz.date_published
            print quiz.date_closed
            new_quiz = {}
            new_quiz['id'] = quiz.id
            new_quiz['datetime'] = datetime.strptime( quiz.date_published[:-4], "%Y-%m-%dT%H:%M:%S." ).strftime('%Y-%m-%d %H:%M:%S')
            if quiz.date_closed:
                new_quiz['closedate'] = datetime.strptime( quiz.date_closed[:-4], "%Y-%m-%dT%H:%M:%S." ).strftime('%Y-%m-%d %H:%M:%S')
            else:
                new_quiz['closedate'] = None
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
            question_answers = []
            for key, value in request.POST.iteritems():
                if key.lower().startswith('question{0}answer'.format(i+1)) and key != 'question{0}AnswersTrue'.format(i+1):
                    question_answers.append(key)
            question_answers.sort()
            answers = [request.POST[key] for key in question_answers]
            correctAnswerIndex = int(request.POST['question{0}AnswersTrue'.format(i+1)])-1
            questions.append({"question":question, "choices":answers, "correct":correctAnswerIndex})
        quiz = {"title": title, "description": description, "course_id": course_id, "questions": questions}
        r = requests.post(REST_API+url, data=json.dumps(quiz), headers={'content-type': 'application/json'},
                          auth=(email, password))
        if r.status_code == requests.codes.created:
            return redirect(reverse('course_page', args=[course_id]))
        else:
            return server_error(request)
    return render(request, 'courses/add_quiz.html')

def publish_quiz(request, course_id, quiz_id):
    url ='/quizzes/{0}/publish'.format(quiz_id)
    r = submit_quiz(request, course_id, quiz_id, url)
    return r

def close_quiz(request, course_id, quiz_id):
    url ='/quizzes/{0}/close'.format(quiz_id)
    r = submit_quiz(request, course_id, quiz_id, url)
    return r

def submit_quiz(request, course_id, quiz_id, url):
    email = request.session['email']
    password = request.session['password']
    if request.method == 'POST':
        text = request.POST["text"]
        r = requests.post(REST_API + url, data={'message': text}, auth=(email, password))
        if r.status_code == requests.codes.ok:
            json_data = json.dumps({"response":"ok","quiz_id":quiz_id})
        else:
            json_data = json.dumps({"response":"failed","quiz_id":quiz_id})
    r = HttpResponse(json_data, content_type = "application/json")
    return r

def quiz_page(request, course_id, quiz_id):
    url='/statistics/{0}/grade_distribution'.format(quiz_id)
    accept_json_header = {'accept': 'application/json'}
    email = request.session['email']
    password = request.session['password']
    r = requests.get(REST_API+url, headers=accept_json_header, auth=(email, password))
    if r.status_code != requests.codes.ok:
        server_error(request)
    grade_distribution = r.json()
    quiz_title = grade_distribution["quiz_title"]
    total_participants = grade_distribution['total_participants']
    quiz_id = grade_distribution["quiz_id"]

    url = '/quizzes/{0}/questions'.format(quiz_id)
    r = requests.get(REST_API+url, headers=accept_json_header, auth=(email, password))

    questions = r.json(object_hook=json_object_hook)
    if r.status_code != requests.codes.ok:
        server_error(request)
    return render(request, 'courses/quiz.html', {'title':quiz_title, 'quiz_id':quiz_id,
                                                 'total_participants': total_participants,
                                                 'questions':questions})

def quiz_statistics(request, quiz_id):
    url='/statistics/{0}/grade_distribution'.format(quiz_id)
    accept_json_header = {'accept': 'application/json'}
    email = request.session['email']
    password = request.session['password']
    r = requests.get(REST_API+url, headers=accept_json_header, auth=(email, password))
    grade_distribution = r.json()
    X = []
    Y = []
    for pair in grade_distribution['grade_distribution']:
        if pair['count']!=0:
            Y.append(pair['count'])
        else:
            Y.append(0.01)
        X.append(pair['score']*100)
    ed_chart = pygal.StackedBar(legend_at_bottom=True, title_font_size=10, legend_font_size=10,
                                style=custom_style, width=600, height=300,
                                js= PYGAL_JS_FILES)
    ed_chart.title = "General progress of students"
    ed_chart.add('Number of students', Y)
    ed_chart.x_labels = [u"{0}%".format(x) for x in X]
    temp = tempfile.NamedTemporaryFile('rw')
    ed_chart.render_to_file(temp.name)
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='image/svg+xml')
    return response

def questions_statistics(request, quiz_id):
    url='/statistics/{0}/answers_distribution'.format(quiz_id)
    accept_json_header = {'accept': 'application/json'}
    email = request.session['email']
    password = request.session['password']
    r = requests.get(REST_API+url, headers=accept_json_header, auth=(email, password))
    answers_distribution = r.json()
    total_submissions = answers_distribution['total_submissions']
    correct_answers_count = []
    wrong_answers_count = []
    not_answered_count = []
    num_question = 0
    #X = xrange(1,15)
    #Y = [x*10%6 for x in xrange(1,15)]
    for question in answers_distribution['answers_distribution']:
        if question['correct_answers_count'] == 0:
            correct_answers_count.append(0.01)
        else:
            correct_answers_count.append(question['correct_answers_count'])
        if question['wrong_answers_count'] == 0:
            wrong_answers_count.append(0.01)
        else:
            wrong_answers_count.append(question['wrong_answers_count'])
        if question['not_answered_count'] == 0:
            not_answered_count.append(0.01)
        else:
            not_answered_count.append(question['not_answered_count'])
        num_question = num_question+1

    ed_chart = pygal.Bar(legend_at_bottom=True, title_font_size=10, legend_font_size=10,
                                style=question_style, width=600, height=300, order_min = 0, show_x_guides =True,
                                js= PYGAL_JS_FILES)
    pygal.print_zeros = True
    ed_chart.title = "Per question results"
    X = xrange(1,num_question+1)
    ed_chart.x_labels = [u"Q.{0}".format(x) for x in X]
    ed_chart.add('Number of correct answers', correct_answers_count)
    ed_chart.add('Number of not answered', not_answered_count)
    ed_chart.add('Number of wrong answers', wrong_answers_count)
    temp = tempfile.NamedTemporaryFile('rw')
    ed_chart.render_to_file(temp.name)
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='image/svg+xml')
    return response

def motivation_statistics(request, quiz_id):
    url='/statistics/{0}/submissions_dates'.format(quiz_id)
    accept_json_header = {'accept': 'application/json'}
    email = request.session['email']
    password = request.session['password']
    r = requests.get(REST_API+url, headers=accept_json_header, auth=(email, password))
    distribution = r.json()
    date_published = distribution['date_published']
    date_published = datetime.strptime( date_published[:-4], "%Y-%m-%dT%H:%M:%S." )
    middle=0
    short=0
    long=0
    for submission in distribution['submissions']:
        date = submission['date_submitted']
        date = datetime.strptime( date[:-4], "%Y-%m-%dT%H:%M:%S." )
        difference = date.date()-date_published.date()
        delta= abs(difference.days)
        if delta <= 1:
            short = short+1
        elif delta <=3:
            middle = middle+1
        else:
            long = long+1
    pie_chart = pygal.Pie(legend_at_bottom=True, title_font_size=10, legend_font_size=10,
                                style=motivation_style, width=600, height=300,
                                js= PYGAL_JS_FILES)
    pie_chart.title = 'Motivation (in %)'
    pie_chart.add('1< day <3', middle)
    pie_chart.add('< 1 day', short)
    pie_chart.add('In the last day', long)

    temp = tempfile.NamedTemporaryFile('rw')
    pie_chart.render_to_file(temp.name)
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='image/svg+xml')
    return response