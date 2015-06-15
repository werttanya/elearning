import re
from django import forms
attrsdict = {'class': 'required'}
alnum_re = re.compile(r'^\w+$')

class SiteForm(forms.Form):
    """
    Extended :class:`Form` object. Removes 'default :' after labels on the
    form.
    """
    def __init__(self, *args, **kwargs):
        # eliminate the colon (:) that is automatically added to form labels
        kwargs.setdefault('label_suffix', '')
        super(SiteForm, self).__init__(*args, **kwargs)


class RegistrationForm(SiteForm):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrsdict,
                                                               maxlength=75)),
                             label=u'email address')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrsdict, render_value=False),
                                label=u'password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrsdict, render_value=False),
                                label=u'password (again)')
    firstname = forms.CharField(widget=forms.TextInput(attrs=attrsdict),
                                 label=u'first name')
    lastname = forms.CharField(widget=forms.TextInput(),
                                label=u'last name')

    def clean_firstname(self):
        """
        Return a copy of the field 'name' with leading and trailing
        whitespace removed.
        """
        value = self.cleaned_data.get('firstname', '')
        value = value.strip()
        return value

    def clean_lastname(self):
        """
        Return a copy of the field 'name' with leading and trailing
        whitespace removed.
        """
        value = self.cleaned_data.get('lastname', '')
        value = value.strip()
        return value

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u'You must type the same password each time')
        return self.cleaned_data

class LoginForm(SiteForm):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrsdict,
                                                               maxlength=75)),
                             label=u'email address')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrsdict, render_value=False),
                                label=u'password')