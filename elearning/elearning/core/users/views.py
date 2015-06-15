import requests
from .forms import RegistrationForm, LoginForm, add_form_error
from django.shortcuts import redirect, render
from elearning.settings import REST_API
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse

def user_login_required(function):
    def wrap(request, *args, **kwargs):
        # this check the session if email and password exist,
        # if not it will redirect to login page
        if 'email' not in request.session.keys() or 'password' not in request.session.keys():
            return HttpResponseRedirect(reverse("login"))
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid() and (request.POST['password1'] == request.POST['password2']):
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            params = {'firstname': firstname, 'lastname': lastname, 'email': email, 'password': password}
            url = '/users'
            r = requests.post(REST_API+url, data=params)
            if r.status_code == requests.codes.created:
                request.session["email"] = email
                request.session["password"] = password
                courses_url = '/courses/'
                return redirect(courses_url)
            else:
                return HttpResponseBadRequest()
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form,})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            url='/account/authored'
            accept_json_header = {'accept': 'application/json'}
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            r = requests.get(REST_API+url, headers=accept_json_header, auth=(email, password))
            if r.status_code != requests.codes.unauthorized:
                request.session["email"] = email
                request.session["password"] = password
                return redirect(reverse('courses'))
            else:
                add_form_error(form, "password", "wrong password")

    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form,})

def logout(request):
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return redirect(reverse('login'))