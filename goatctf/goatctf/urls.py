from django.conf.urls import patterns, include, url
from django.contrib import admin
import core.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'goatctf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'', include(core.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
