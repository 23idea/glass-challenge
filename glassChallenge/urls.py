from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
    #url(r'^$', 'glassChallenge.views.home', name='home'),
    #url(r'^glassChallenge/', include('glassChallenge.foo.urls')),
    url(r'^google/login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
    url(r'^google/login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('challenge.urls'))
)
