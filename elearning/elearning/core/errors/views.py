from django.shortcuts import render


def bad_request(request):
    """
    Bad request view. Generates `errors/400.html` template.

    :param: :class:`Request` object
    :returns: :class:`HTTPResponse` object
    """
    return render(request, 'errors/400.html', status=400)


def permission_denied(request):
    """
    Permission denied view. Generates `errors/403.html` template.

    :param: :class:`Request` object
    :returns: :class:`HTTPResponse` object
    """
    return render(request, 'errors/403.html', status=403)


def page_not_found(request):
    """
    Page not found view. Generates `errors/404.html` template.

    :param: :class:`Request` object
    :returns: :class:`HTTPResponse` object
    """
    return render(request, 'errors/404.html', status=404)


def server_error(request):
    """
    Internal server error view. Generates `errors/500.html` template.

    :param: :class:`Request` object
    :returns: :class:`HTTPResponse` object
    """
    return render(request, 'errors/500.html', status=500)