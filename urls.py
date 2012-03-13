from django.conf.urls.defaults import patterns
from tardis.urls import urlpatterns as tardisurls
from django.conf import settings

# Use the new views in MicroTardis
urlpatterns = patterns('tardis.microtardis.views',
    # override tardis_portal url patterns
    (r'^experiment/view/(?P<experiment_id>\d+)/(?P<show_hidden>\d+)/$', 'redirect_view_experiment'),
    (r'^ajax/parameters/(?P<dataset_file_id>\d+)/$', 'retrieve_parameters'),
    (r'^ajax/experiment_description/(?P<experiment_id>\d+)/$', 'experiment_description'),
    (r'^ajax/experiment_datasets/(?P<experiment_id>\d+)/$', 'experiment_datasets'),
    (r'^ajax/datafile_list/(?P<dataset_id>\d+)/$', 'retrieve_datafile_list'),
    # microtardis's own url patterns
    (r'^microtardis/spectra_png/(?P<size>[\w\.]+)/(?P<datafile_id>\d+)/(?P<datafile_type>[\w\.]+)/$', 'get_spectra_png'),
    (r'^microtardis/spectra_csv/(?P<datafile_id>\d+)/$', 'get_spectra_csv'),
    (r'^microtardis/spectra_json/(?P<datafile_id>\d+)/$', 'get_spectra_json'),
    (r'^microtardis/thumbnails/(?P<size>[\w\.]+)/(?P<datafile_id>[\w\.]+)/$', 'display_thumbnails'),
    (r'^microtardis/(?P<datafile_id>\d+)/(?P<datafile_type>[\w\.]+)/$', 'direct_to_thumbnail_html'),
    (r'^microtardis/hide/$', 'hide_objects'),
    (r'^microtardis/unhide/$', 'unhide_objects'),
)

# Media for MicroTardis
urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MT_STATIC_DOC_ROOT}),
)

# Use the new templates in MicroTardis but still use the original views in MyTardis
#urlpatterns += patterns('tardis.tardis_portal.views',
#    (r'^ajax/datafile_list/(?P<dataset_id>\d+)/$', 'retrieve_datafile_list', {'template_name': 'datafile_list_mt.html'}),
#)

# Include all the URL patterns in MyTardis
urlpatterns += tardisurls
