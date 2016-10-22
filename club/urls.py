from django.conf.urls import url

from . import views
from club.views import *


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<session_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^sessions/$', views.sessions, name='sessions'),

	url(r'^session/(?P<pk>[0-9]+)/detail/$', SessionDetail.as_view(), name='session_detail'),
	url(r'^session/create/$', SessionCreateCustom.as_view(), name='session_create'),
	url(r'^session/create_private/$', SessionCreatePrivateCustom.as_view(), name='session_create_private'),
	url(r'^session/list/$', SessionList.as_view(), name='session_list'),	
	url(r'^session/(?P<pk>[0-9]+)/update/$', SessionUpdate.as_view(), name='session_update'),
	url(r'^session/(?P<pk>[0-9]+)/delete/$', SessionDelete.as_view(), name='session_delete'),
	url(r'^session/(?P<pk>[0-9]+)/assign_player/$', SessionAssignPlayer.as_view(), name='session_assign_player'),
	url(r'^session/(?P<pk>[0-9]+)/assign_instructor/$', SessionAssignInstructor.as_view(), name='session_assign_instructor'),

	url(r'^player/(?P<pk>[0-9]+)/detail/$', PlayerDetail.as_view(), name='person_detail'),

	#url(r'^person/(?P<pk>[0-9]+)/detail/$', PlayerDetail.as_view(), name='person_detail'),
	url(r'^player/create/$', PlayerCreateCustom.as_view(), name='player_create'),
	url(r'^player/list/$', PlayerList.as_view(), name='player_list'),	
	url(r'^player/(?P<assoc>[a-zA-Z0-9.]+)/sibling1/$', PlayerSiblings.as_view(), name='player_siblings'),
	url(r'^player/(?P<pk>[0-9]+)/siblings/$', PlayerSiblings.as_view(), name='player_siblings'),
	url(r'^player/(?P<pk>[0-9]+)/update/$', PlayerUpdate.as_view(), name='player_update'),
	url(r'^player/(?P<pk>[0-9]+)/delete/$', PlayerDelete.as_view(), name='player_delete'),
	url(r'^player/(?P<pk>[0-9]+)/played_sessions/$', PlayerPlayedSessions.as_view(), name='player_played_sessions'),
	# url(r'^player/(?P<pk>[0-9]+)/report_bill/$', PlayerReportBill.as_view(), name='player_report_bill'),
	
    url(r'^instructor/(?P<pk>[0-9]+)/detail/$', InstructorDetail.as_view(), name='instructor_detail'),
    url(r'^instructor/create/$', InstructorCreate.as_view(), name='instructor_create'),
    url(r'^instructor/list/$', InstructorList.as_view(), name='instructor_list'),	
   


    url(r'^persons/$', views.players, name='players'),
  
  	url(r'^instructors/$', views.instructors, name='instructors'),
    url(r'^person/lessons/(?P<person_id>[0-9]+)/$', views.person_lessons, name='person_lessons'),
    url(r'^person/edit/(?P<person_id>[0-9]+)/$', views.person_edit, name='person_edit'),
    url(r'^instructor/lessons/(?P<instructor_id>[0-9]+)/$', views.instructor_lessons, name='instructor_lessons'),
]
