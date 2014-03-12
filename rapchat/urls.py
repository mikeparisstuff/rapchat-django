from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from users import views as users_views
# from crowds import views as crowds_views
from groupsessions import views as sessions_views
from feedback import views as feedback_views 

admin.autodiscover()

urlpatterns = patterns('',

	url(r'api-docs/', include('rest_framework_swagger.urls')),

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', users_views.WelcomePage.as_view(), name='welcome_page'),

    # USER ENDPOINTS
    url(r'^users/$', users_views.HandleUsers.as_view(), name='create_new_user'),
    url(r'^users/(?P<username>\w{3,50})/$', users_views.HandleUser.as_view(), name='handle_user'),
    url(r'^users/(?P<username>\w{3,50})/likes/$', sessions_views.HandleUserLikes.as_view(), name='handle_user_likes'),
    url(r'^users/me/$', users_views.HandleMyProfile.as_view(), name='get_my_user'),
    url(r'^users/me/likes/$', sessions_views.HandleGroupSessionLikes.as_view(), name='get_my_likes'),
    url(r'^users/me/clips/$', sessions_views.HandleMyGroupSessionClips.as_view(), name='get_my_clips'),
    url(r'^users/obtain-token/$', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^invite/$', users_views.HandleInvites.as_view(), name='invite_users'),
    
    url(r'^search/$', users_views.HandleSearch.as_view(), name='search_users'),

    url(r'^users/me/friends/$', users_views.HandleFriends.as_view(), name='handle_friends'),
    url(r'^users/me/friends/requests/$', users_views.HandleFriendRequests.as_view(), name='handle_friend_requests'),
    url(r'^users/me/friends/requests/reply/$', users_views.HandleFriendRequestReplies.as_view(), name='handle_friend_request_replies'),

    # CROWDS ENDPOINTS
    # url(r'^users/me/crowds/$', crowds_views.HandleCrowds.as_view(), name='handle_crowds'),

    # SESSIONS ENDPOINTS
    url(r'^users/me/sessions/$', sessions_views.HandleGroupSessions.as_view(), name='handle_sessions'),
    url(r'^users/me/sessions/live/$', sessions_views.HandleGroupSessions.as_view(), name='handle_sessions'),
    url(r'^users/me/sessions/complete/$', sessions_views.HandleCompletedGroupSessions.as_view(), name='handle_completed_sessions'),
    url(r'^sessions/(?P<session>\d+)/$', sessions_views.HandleGroupSession.as_view(), name='handle_single_session'),
    url(r'^sessions/(?P<session>\d+)/clips/$', sessions_views.HandleGroupSessionClips.as_view(), name='handle_clips'),
    url(r'^sessions/(?P<session>\d+)/comments/$', sessions_views.HandleGroupSessionComments.as_view(), name='handle_session_comments'),
    # url(r'^sessions/likes/$', sessions_views.HandleSessionLikes.as_view(), name='handle_likes'),

    # BATTLES ENDPOINTS
    # url(r'^users/me/battles/$', sessions_views.HandleBattleSessions.as_view(), name='handle_battles'),
    # url(r'^users/me/battles/complete/$', sessions_views.HandleCompletedBattleSessions.as_view(), name='handle_complete_battles'),
    # url(r'^users/me/battles/likes/$', sessions_views.HandleBattleSessionLikes.as_view(), name='handle_battle_likes'),
    # url(r'^battles/(?P<battle>\d+)/clips/$', sessions_views.HandleBattleSessionClips.as_view(), name='handle_battle_clips'),
    # url(r'^battles/(?P<battle>\d+)/comments/$', sessions_views.HandleBattleSessionComments.as_view(), name='handle_battle_session_comments'),

    url(r'^feedback/$', feedback_views.HandleFeedback.as_view(), name='handle_feedback'),

)
