from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from challenge import views
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    #challenges
    url(r'^submit/$', login_required(views.ChallengeCreate.as_view()), name='challenge_submit'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(views.ChallengeUpdate.as_view()), name='challenge_edit'),
    url(r'^details/(?P<pk>\d+)/$',  views.ChallengeDetail.as_view(), name='challenge_details'),
    #claims
    url(r'^claim/submit/(?P<pk>\d+)/$', login_required(views.ClaimCreate.as_view()), name='claim_submit'),
    url(r'^claim/edit/(?P<pk>\d+)/$', login_required(views.ClaimUpdate.as_view()), name='claim_edit'),
    url(r'^claim/details/(?P<pk>\d+)/$', views.ClaimDetail.as_view(), name='claim_details'),
    #you?
    url(r'^user/(?P<pk>\d+)/$', views.UserView.as_view(), name='user'),
    url(r'^user/edit/$', views.ProfileUpdate.as_view(), name='user_edit'),
    url(r'^vote/$', views.vote, name='vote')
)


if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve')
    )
