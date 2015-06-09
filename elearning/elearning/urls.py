from django.conf.urls import include, url
from django.contrib import admin

# Custom error handlers
handler400 = 'elearning.core.errors.views.bad_request'
handler403 = 'elearning.core.errors.views.permission_denied'
handler404 = 'elearning.core.errors.views.page_not_found'
handler500 = 'elearning.core.errors.views.server_error'

urlpatterns = [
    # Examples:
    # url(r'^$', 'elearning.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include("elearning.core.users.urls"))
]
