from elearning.core.users.forms import SiteForm
from django import forms

class CourseForm(SiteForm):
    """
    Extended :class:`SiteForm` with `title` and `description` fields.
    """
    title = forms.CharField(
        max_length=255, required=True, label=u'Course name'
    )
    description = forms.CharField(
        max_length=5000, required=True, label=u'Course description',
        widget=forms.Textarea()
    )

    def clean_title(self):
        """
        Return a copy of the field 'title' with leading and trailing
        whitespace removed.
        """
        value = self.cleaned_data.get('title', '')
        value = value.strip()
        return value