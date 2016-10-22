	url(r'^player/(?P<pk>[0-9]+)/detail/$', PlayerDetail.as_view(), name='player_detail'),
	url(r'^person/(?P<pk>[0-9]+)/detail/$', PlayerDetail.as_view(), name='person_detail'),
	url(r'^player/create/$', PlayerCreate.as_view(), name='player_create'),
	url(r'^player/list/$', PlayerList.as_view(), name='player_list'),	
	url(r'^player/(?P<pk>[0-9]+)/update/$', PlayerUpdate.as_view(), name='player_update'),
	url(r'^player/(?P<pk>[0-9]+)/delete/$', PlayerDelete.as_view(), name='player_delete'),
	# url(r'^player/(?P<pk>[0-9]+)/report_bill/$', PlayerReportBill.as_view(), name='player_report_bill'),
	