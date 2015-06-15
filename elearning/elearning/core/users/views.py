import requests
from .forms import RegistrationForm, LoginForm
from django.shortcuts import redirect, render
from elearning.settings import REST_API
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse

def user_login_required(request, *args, **kwargs):
    # this check the session if email and password exist,
    # if not it will redirect to login page
    if 'email' not in request.session.keys() or 'password' not in request.session.keys():
        return HttpResponseRedirect(reverse("login"))
    return True

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
            pass
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form,})