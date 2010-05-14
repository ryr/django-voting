from django.conf.urls.defaults import *


urlpatterns = patterns('voting.views',
    # for voting objects
    url(r'^vote/$', 'vote_on_object', name='vote'),
)
