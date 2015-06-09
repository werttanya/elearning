from django.template import Library

register = Library()


@register.inclusion_tag('form_error.html')
def show_field_error(errors):
    return {'errors': errors}


@register.inclusion_tag('single_error.html')
def show_single_error(error):
    return {'error': error}




