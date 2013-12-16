from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from users import views as users_views
from crowds import views as crowds_views
from groupsessions import views as sessions_views

admin.autodiscover()

urlpatterns = patterns('',

	url(r'api-docs/', include('rest_framework_swagger.urls')),

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', users_views.WelcomePage.as_view(), name='welcome_page'),

    # USER ENDPOINTS
    url(r'^users/$', users_views.HandleUsers.as_view(), name='create_new_user'),
    url(r'^users/me/$', users_views.HandleMyProfile.as_view(), name='get_my_user'),
    url(r'^users/obtain-token/$', 'rest_framework.authtoken.views.obtain_auth_token'),

    url(r'^users/friends/$', users_views.HandleFriends.as_view(), name='handle_friends'),
    url(r'^users/friends/requests/$', users_views.HandleFriendRequests.as_view(), name='handle_friend_requests'),
    url(r'^users/friends/requests/reply/$', users_views.HandleFriendRequestReplies.as_view(), name='handle_friend_request_replies'),

    # CROWDS ENDPOINTS
    url(r'^crowds/$', crowds_views.HandleCrowds.as_view(), name='handle_crowds'),

    # SESSIONS ENDPOINTS
    url(r'^sessions/$', sessions_views.HandleSessions.as_view(), name='handle_sessions'),
    url(r'^sessions/addclip/$', sessions_views.HandleClips.as_view(), name='handle_clips'),
    url(r'^sessions/comments/$', sessions_views.HandleSessionComments.as_view(), name='handle_session_comments'),
    url(r'^sessions/comments/(?P<session>\d+)/$', sessions_views.HandleSessionComments.as_view(), name='handle_session_comments'),
    url(r'^sessions/likes/$', sessions_views.HandleSessionLikes.as_view(), name='handle_likes'),
)
