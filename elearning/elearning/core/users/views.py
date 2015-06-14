import requests
from .forms import RegistrationForm
from django.shortcuts import redirect, render
from elearning.settings import REST_API
from django.http import HttpResponseBadRequest

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
