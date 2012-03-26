import os
import Image
import imghdr
import struct
import csv
import StringIO
import numpy
import urllib2
import hashlib
import json
import sys

from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.utils import simplejson as json
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
# for experiment_description
from django.contrib.auth.models import User
# for retrieve_datafile_list
from django.core.paginator import Paginator
from urllib import urlencode
# for login
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import Permission

from tardis.tardis_portal.auth import decorators as authz
from tardis.tardis_portal.shortcuts import render_response_index
from tardis.tardis_portal.staging import add_datafile_to_dataset
from tardis.tardis_portal.staging import write_uploaded_file_to_dataset
# for experiment_description
from tardis.tardis_portal.auth.localdb_auth import django_user
# for experiment_datasets
from tardis.tardis_portal.views import getNewSearchDatafileSelectionForm
# for login
from tardis.tardis_portal.forms import LoginForm
from tardis.tardis_portal.auth import login as tardis_login
from tardis.tardis_portal.auth import auth_service
from tardis.tardis_portal.auth.utils import get_or_create_user

from tardis.tardis_portal.models import DatafileParameterSet
from tardis.tardis_portal.models import Schema
from tardis.tardis_portal.models import Dataset
from tardis.tardis_portal.models import Dataset_File
# for experiment_description
from tardis.tardis_portal.models import Experiment
from tardis.tardis_portal.models import ExperimentACL
# for login
from tardis.tardis_portal.models import UserProfile
from tardis.tardis_portal.models import UserAuthentication

from tardis.microtardis.models import Experiment_Hidden
from tardis.microtardis.models import Dataset_Hidden
from tardis.microtardis.models import Datafile_Hidden
from tardis.microtardis.models import Dataset_Harvest
from tardis.microtardis.models import Datafile_Harvest

# for view_experiment
from tardis.urls import getTardisApps

# import and configure matplotlib library
try:
    os.environ['HOME'] = settings.MATPLOTLIB_HOME
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as pyplot
    is_matplotlib_imported = True
except ImportError:
    is_matplotlib_imported = False
    

@never_cache
@authz.datafile_access_required
def retrieve_parameters(request, dataset_file_id):
    # get schema id of EDAX Genesis spectra schema
    schema_spc = Schema.objects.filter(name="EDAXGenesis_SPC")
    schema_ids_spc = []
    for schema in schema_spc:
        schema_ids_spc.append(schema.id)
    field_order_spc = ["Sample Type (Label)", "Preset", "Live Time", "Acc. Voltage"]
    
    # get schema id of EXIF image metadata schema
    schema_exif = Schema.objects.filter(name__endswith="EXIF")
    schema_ids_exif = []
    for schema in schema_exif:
        schema_ids_exif.append(schema.id)
    field_order_exif = ["[User] Date", "[User] Time"]

    datafileparametersets = DatafileParameterSet.objects.filter(dataset_file__pk=dataset_file_id)
    parametersets = {}
    for parameterset in datafileparametersets:
        unsorted = {}
        sorted = []
        # get list of parameters
        parameters = parameterset.datafileparameter_set.all()
        for parameter in parameters:
            unsorted[str(parameter.name.full_name)] = parameter
                
        # sort spectra tags
        if parameterset.schema.id in schema_ids_spc:
            # sort spectra tags defined in field_order_spc                
            for field in field_order_spc:
                if field in unsorted:
                    sorted.append(unsorted[field])
                    unsorted.pop(field)
            # sort atomic peak numbers
            peaks = []
            for field in unsorted:
                if field.startswith("Peak ID Element"):
                    peaks.append(field)
            peaks.sort(key=lambda peak: int(peak.split(" ")[-1])) 
            for field in peaks:
                sorted.append(unsorted[field])
                unsorted.pop(field)
            # sort the rest of unsorted parameters
            if unsorted:
                sorted_keys = unsorted.keys()
                sorted_keys.sort()
                for key in sorted_keys:
                    sorted.append(unsorted[key])
            parametersets[parameterset.schema] = sorted
        # sort exif tags
        elif parameterset.schema.id in schema_ids_exif:
            # sort exif metadata tags defined in field_order_exif
            for field in field_order_exif:
                if field in unsorted:
                    sorted.append(unsorted[field])
                    unsorted.pop(field)
            # sort the rest of unsorted parameters
            if unsorted:
                sorted_keys = unsorted.keys()
                sorted_keys.sort()
                for key in sorted_keys:
                    sorted.append(unsorted[key])
            parametersets[parameterset.schema] = sorted
        # use default order
        else:
            parametersets[parameterset.schema] = parameters
    
    thumbpath = None
    file_type = False
    qs = Dataset_File.objects.filter(id=dataset_file_id)
    if qs:
        datafile = qs[0]
        # for showing spectra image
        if str(datafile.filename)[-4:] == ".spc":
            file_type = "spc"
        elif str(datafile.filename)[-4:] == ".spt":
            file_type = "spt"
        # .tif thumbnail image
        elif datafile.mimetype == "image/tiff":
            basepath = "/thumbnails/small"
            thumbname = str(datafile.id)
            thumbpath = os.path.join(basepath, thumbname)

    c = Context({'parametersets': parametersets,
                 'thumbpath': thumbpath,
                 'file_type': file_type,
                 'datafile_id': dataset_file_id})

    return HttpResponse(render_response_index(request,
                        'tardis_portal/ajax/parameters.html', c))


def login(request):
    
    if type(request.user) is not AnonymousUser:
        return HttpResponseRedirect('/')

    c = Context({'loginForm': LoginForm()})
    
    # get POST and GET variables
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    authMethod = request.POST.get('authMethod', '')
    next = request.GET.get('next', '/')
    
    if not username or not password:
        # show login form
        return HttpResponse(render_response_index(request, 'tardis_portal/login.html', c))
    
    #authenticate user in mytardis localdb
    user = auth_service.authenticate(authMethod=authMethod, request=request)
    user_exist = None
    try:
        user_exist = User.objects.get(username=username)
    except User.DoesNotExist:
        pass
    # check the existence of user
    if user:
        # user existed and authentication passed
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        tardis_login(request, user)
        return HttpResponseRedirect(next)
    elif user_exist:
        # user existed but authentication failed
        c['status'] = "Sorry, username and password don't match."
        c['error'] = True
        return HttpResponseForbidden( render_response_index(request, 'tardis_portal/login.html', c))
    else:
        # user doesn't exist, create one if EMBS authentication succeeded
        
        # authenticate username and password with EMBS system
        embs_url = settings.EMBS_URL
        embs_url += "username=%s&passwordmd5=%s" % ( str(username).lower(), 
                                                     hashlib.md5(password).hexdigest() )
        try:
            response = urllib2.urlopen(embs_url).read()
            if response.status() == 200:
#            dummy_status = 200
#            dummy_json = """
#{"user_id":       "1",
# "fname":         "e123",
# "lname":         "e123",
# "title":         "mr",
# "department":    "rmmf",
# "login_name":    "e123",
# "email":         "e123@e123.com",
# "phone":         "12345",
# "user_type":     "student",
# "user_category": "student" } """
#            if dummy_status == 200:
                # succeeded authentication
                # create new user and userprofile into mytardis localdb
                user_json = json.loads(response.read())
#                user_json = json.loads(dummy_json)
                email = user_json['email']
                first_name = user_json['fname']
                last_name = user_json['lname']
                user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email)
                user.first_name = first_name
                user.last_name = last_name
                user.user_permissions.add(Permission.objects.get(codename='add_experiment'))
                user.user_permissions.add(Permission.objects.get(codename='change_experiment'))
                user.user_permissions.add(Permission.objects.get(codename='change_experimentacl'))
                user.user_permissions.add(Permission.objects.get(codename='change_group'))
                user.user_permissions.add(Permission.objects.get(codename='change_userauthentication'))
                user.save()

                userProfile = UserProfile(user=user, isDjangoAccount=False)
                userProfile.save()
            
                userAuth = UserAuthentication(userProfile=userProfile,
                                              username=username, 
                                              authenticationMethod=authMethod)
                userAuth.save()
                
                # log in with valid user
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                tardis_login(request, user)
                return HttpResponseRedirect(next)
            else:
                # authentication failed
                c['status'] = "Sorry, username and password don't match."
                c['error'] = True
                return HttpResponseForbidden( render_response_index(request, 'tardis_portal/login.html', c))
        except urllib2.URLError, e:
            c['status'] = "Sorry, error happened with EMBS authentication: %s" % e
            c['error'] = True

    return HttpResponseForbidden( render_response_index(request, 'tardis_portal/login.html', c))


@never_cache
@authz.experiment_access_required
def redirect_view_experiment(request, experiment_id, show_hidden):
    show_hidden = int(show_hidden)
    if show_hidden == 0:
        request.session['session_show_hidden'] = False
        request.session['session_hidden_text'] = "Show Hidden Datasets and Files"
    elif show_hidden == 1:
        request.session['session_show_hidden'] = True
        request.session['session_hidden_text'] = "Hide Hidden Datasets and Files"
        
    return HttpResponseRedirect(reverse('tardis.microtardis.views.view_experiment', args=(experiment_id,)))


@authz.experiment_access_required
def view_experiment(request, experiment_id):

    """View an existing experiment.

    :param request: a HTTP Request instance
    :type request: :class:`django.http.HttpRequest`
    :param experiment_id: the ID of the experiment to be edited
    :type experiment_id: string
    :rtype: :class:`django.http.HttpResponse`

    """
    c = Context({})

    try:
        experiment = Experiment.safe.get(request, experiment_id)
    except PermissionDenied:
        return return_response_error(request)
    except Experiment.DoesNotExist:
        return return_response_not_found(request)

# microtardis change start
    if 'session_show_hidden' not in request.session:
        request.session['session_show_hidden'] = False
    if 'session_hidden_text' not in request.session:
        request.session['session_hidden_text'] = "Show Hidden Datasets and Files"
    
    if not request.session['session_show_hidden']:
        # hide hidden objects
        hidden_datasets = Dataset_Hidden.objects.filter(hidden=True).values_list('dataset', flat=True)
        c['datasets'] = Dataset.objects.filter(experiment=experiment_id).exclude(pk__in=hidden_datasets)
    else:
        # show all datasets
        c['datasets'] = Dataset.objects.filter(experiment=experiment_id)
# microtardis change end

    c['experiment'] = experiment
    c['has_write_permissions'] = \
        authz.has_write_permissions(request, experiment_id)
    if request.user.is_authenticated():
        c['is_owner'] = authz.has_experiment_ownership(request, experiment_id)
    c['subtitle'] = experiment.title
    c['nav'] = [{'name': 'Data', 'link': '/experiment/view/'},
                {'name': experiment.title,
                 'link': experiment.get_absolute_url()}]

    if 'status' in request.POST:
        c['status'] = request.POST['status']
    if 'error' in request.POST:
        c['error'] = request.POST['error']
    if 'query' in request.GET:
        c['search_query'] = SearchQueryString(request.GET['query'])
    if  'search' in request.GET:
        c['search'] = request.GET['search']
    if  'load' in request.GET:
        c['load'] = request.GET['load']

    import sys
    appnames = []
    appurls = []
    for app in getTardisApps():
        try:
            appnames.append(sys.modules['%s.%s.settings'
                                        % (settings.TARDIS_APP_ROOT, app)].NAME)
            appurls.append('%s.%s.views.index' % (settings.TARDIS_APP_ROOT, app))
        except:
            pass

    c['apps'] = zip(appurls, appnames)

    return HttpResponse(render_response_index(request,
                        'tardis_portal/view_experiment.html', c))


@authz.experiment_access_required
def experiment_description(request, experiment_id):
    """View an existing experiment's description. To be loaded via ajax.

    :param request: a HTTP Request instance
    :type request: :class:`django.http.HttpRequest`
    :param experiment_id: the ID of the experiment to be edited
    :type experiment_id: string
    :rtype: :class:`django.http.HttpResponse`

    """
    c = Context({})

    try:
        experiment = Experiment.safe.get(request, experiment_id)
    except PermissionDenied:
        return return_response_error(request)
    except Experiment.DoesNotExist:
        return return_response_not_found(request)

    c['experiment'] = experiment
    c['subtitle'] = experiment.title
    c['nav'] = [{'name': 'Data', 'link': '/experiment/view/'},
                {'name': experiment.title,
                 'link': experiment.get_absolute_url()}]

    c['authors'] = experiment.author_experiment_set.all()

# microtardis change start
    if 'session_show_hidden' not in request.session:
        request.session['session_show_hidden'] = False
    if 'session_hidden_text' not in request.session:
        request.session['session_hidden_text'] = "Show Hidden Datasets and Files"
        
    if not request.session['session_show_hidden']:
        # hide hidden objects
        hidden_datasets = Dataset_Hidden.objects.filter(hidden=True).values_list('dataset', flat=True)
        c['datasets'] = Dataset.objects.filter(experiment=experiment_id).exclude(pk__in=hidden_datasets)
        hidden_datafiles = Datafile_Hidden.objects.filter(hidden=True).values_list('datafile', flat=True)
        c['datafiles'] = Dataset_File.objects.filter(dataset__experiment=experiment_id).exclude(pk__in=hidden_datafiles)
    else:
        # show all objects
        c['datasets'] = Dataset.objects.filter(experiment=experiment_id)
        c['datafiles'] = Dataset_File.objects.filter(dataset__experiment=experiment_id)
# microtardis change end

    acl = ExperimentACL.objects.filter(pluginId=django_user,
                                       experiment=experiment,
                                       isOwner=True)

    # TODO: resolve usernames through UserProvider!
    # Right now there are exceptions every time for ldap users..
    c['owners'] = []
    for a in acl:
        try:
            c['owners'].append(User.objects.get(pk=str(a.entityId)))
        except User.DoesNotExist:
            #logger.exception('user for acl %i does not exist' % a.id)
            pass

    # calculate the sum of the datafile sizes
    size = 0
    for df in c['datafiles']:
        try:
            size = size + long(df.size)
        except:
            pass
    c['size'] = size

    c['has_read_or_owner_ACL'] = \
        authz.has_read_or_owner_ACL(request, experiment_id)

    c['has_write_permissions'] = \
        authz.has_write_permissions(request, experiment_id)

    if request.user.is_authenticated():
        c['is_owner'] = authz.has_experiment_ownership(request, experiment_id)

    c['protocol'] = []
    download_urls = experiment.get_download_urls()
    for key, value in download_urls.iteritems():
        c['protocol'] += [[key, value]]

    if 'status' in request.GET:
        c['status'] = request.GET['status']
    if 'error' in request.GET:
        c['error'] = request.GET['error']

    return HttpResponse(render_response_index(request,
                        'tardis_portal/ajax/experiment_description.html', c))


@never_cache
@authz.experiment_access_required
def experiment_datasets(request, experiment_id):

    """View a listing of dataset of an existing experiment as ajax loaded tab.

    :param request: a HTTP Request instance
    :type request: :class:`django.http.HttpRequest`
    :param experiment_id: the ID of the experiment to be edited
    :type experiment_id: string
    :param template_name: the path of the template to render
    :type template_name: string
    :rtype: :class:`django.http.HttpResponse`

    """
    c = Context({'upload_complete_url':
                     reverse('tardis.tardis_portal.views.upload_complete'),
                 'searchDatafileSelectionForm':
                     getNewSearchDatafileSelectionForm(),
                 })

    try:
        experiment = Experiment.safe.get(request, experiment_id)
    except PermissionDenied:
        return return_response_error(request)
    except Experiment.DoesNotExist:
        return return_response_not_found(request)

    c['experiment'] = experiment
    if 'query' in request.GET:

        # We've been passed a query to get back highlighted results.
        # Only pass back matching datafiles
        #
        search_query = FacetFixedSearchQuery(backend=HighlightSearchBackend())
        sqs = SearchQuerySet(query=search_query)
        query = SearchQueryString(request.GET['query'])
        facet_counts = sqs.raw_search(query.query_string() + ' AND experiment_id_stored:%i' % (int(experiment_id)), end_offset=1).facet('dataset_id_stored').highlight().facet_counts()
        if facet_counts:
            dataset_id_facets = facet_counts['fields']['dataset_id_stored']
        else:
            dataset_id_facets = []

        c['highlighted_datasets'] = [ int(f[0]) for f in dataset_id_facets ]
        c['file_matched_datasets'] = []
        c['search_query'] = query

        # replace '+'s with spaces
    elif 'datafileResults' in request.session and 'search' in request.GET:
        c['highlighted_datasets'] = None
        c['highlighted_dataset_files'] = [r.pk for r in request.session['datafileResults']]
        c['file_matched_datasets'] = \
            list(set(r.dataset.pk for r in request.session['datafileResults']))
        c['search'] = True

    else:
        c['highlighted_datasets'] = None
        c['highlighted_dataset_files'] = None
        c['file_matched_datasets'] = None

# microtardis change start
    if 'session_show_hidden' not in request.session:
        request.session['session_show_hidden'] = False
    if 'session_hidden_text' not in request.session:
        request.session['session_hidden_text'] = "Show Hidden Datasets and Files"
        
    if not request.session['session_show_hidden']:
        # hide hidden objects
        hidden_datasets = Dataset_Hidden.objects.filter(hidden=True).values_list('dataset', flat=True)
        c['datasets'] = Dataset.objects.filter(experiment=experiment_id).exclude(pk__in=hidden_datasets)
        hidden_datafiles = Datafile_Hidden.objects.filter(hidden=True).values_list('datafile', flat=True)
        datafiles = {}
        for dataset in c['datasets']:
            datafiles[dataset] = Dataset_File.objects.filter(dataset=dataset.id).exclude(pk__in=hidden_datafiles).count()
        c['datafiles'] = datafiles
    else:
        # show all objects
        c['datasets'] = Dataset.objects.filter(experiment=experiment_id)
        datafiles = {}
        for dataset in c['datasets']:
            datafiles[dataset] = Dataset_File.objects.filter(dataset=dataset.id).count()
        c['datafiles'] = datafiles
        # highlight hidden datasets
        hidden_datasets = Dataset_Hidden.objects.filter(hidden=True).values_list('dataset', flat=True)
        dataset_objects = Dataset.objects.filter(experiment=experiment_id, pk__in=hidden_datasets)
        c['linethrough_datasets'] = [ obj.pk for obj in dataset_objects ]
        # highlight datasets which have hidden datafiles
        hidden_datafiles = Datafile_Hidden.objects.filter(hidden=True).values_list('datafile', flat=True)
        experiment_dataset_objects = Dataset.objects.filter(experiment=experiment_id)
        hidden_datafiles_objects = Dataset_File.objects.filter(pk__in=hidden_datafiles, dataset__in=experiment_dataset_objects)
        c['file_hidden_datasets'] = list(set(obj.dataset.pk for obj in hidden_datafiles_objects))
# microtardis change end

    c['has_write_permissions'] = \
        authz.has_write_permissions(request, experiment_id)

    c['protocol'] = []
    download_urls = experiment.get_download_urls()
    for key, value in download_urls.iteritems():
        c['protocol'] += [[key, value]]

    if 'status' in request.GET:
        c['status'] = request.GET['status']
    if 'error' in request.GET:
        c['error'] = request.GET['error']

    return HttpResponse(render_response_index(request,
                        'tardis_portal/ajax/experiment_datasets.html', c))


@never_cache
@authz.dataset_access_required
def retrieve_datafile_list(request, dataset_id, template_name='tardis_portal/ajax/datafile_list.html'):

    params = {}

    query = None
    highlighted_dsf_pks = []

    if 'query' in request.GET:
        search_query = FacetFixedSearchQuery(backend=HighlightSearchBackend())
        sqs = SearchQuerySet(query=search_query)
        query =  SearchQueryString(request.GET['query'])
        results = sqs.raw_search(query.query_string() + ' AND dataset_id_stored:%i' % (int(dataset_id))).load_all()
        highlighted_dsf_pks = [int(r.pk) for r in results if r.model_name == 'dataset_file' and r.dataset_id_stored == int(dataset_id)]

        params['query'] = query.query_string()

    elif 'datafileResults' in request.session and 'search' in request.GET:
        highlighted_dsf_pks = [r.pk for r in request.session['datafileResults']]

    dataset_results = \
        Dataset_File.objects.filter(
            dataset__pk=dataset_id,
        ).order_by('filename')
        
# microtardis change start
    if 'session_show_hidden' not in request.session:
        request.session['session_show_hidden'] = False
    if 'session_hidden_text' not in request.session:
        request.session['session_hidden_text'] = "Show Hidden Datasets and Files"
        
    if not request.session['session_show_hidden']:
        # hide hidden objects
        hidden_datafiles = Datafile_Hidden.objects.filter(hidden=True).values_list('datafile', flat=True)
        dataset_results = dataset_results.exclude(pk__in=hidden_datafiles)
# microtardis change end

    if request.GET.get('limit', False) and len(highlighted_dsf_pks):
        dataset_results = \
        dataset_results.filter(pk__in=highlighted_dsf_pks)
        params['limit'] = request.GET['limit']

    filename_search = None

    if 'filename' in request.GET and len(request.GET['filename']):
        filename_search = request.GET['filename']
        dataset_results = \
            dataset_results.filter(url__icontains=filename_search)

        params['filename'] = filename_search

    # pagination was removed by someone in the interface but not here.
    # need to fix.
    pgresults = 100

    paginator = Paginator(dataset_results, pgresults)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.

    try:
        dataset = paginator.page(page)
    except (EmptyPage, InvalidPage):
        dataset = paginator.page(paginator.num_pages)

    is_owner = False
    has_write_permissions = False

    if request.user.is_authenticated():
        experiment_id = Experiment.objects.get(dataset__id=dataset_id).id
        is_owner = authz.has_experiment_ownership(request, experiment_id)

        has_write_permissions = \
            authz.has_write_permissions(request, experiment_id)

    immutable = Dataset.objects.get(id=dataset_id).immutable

    params = urlencode(params)

    c = Context({
        'dataset': dataset,
        'paginator': paginator,
        'immutable': immutable,
        'dataset_id': dataset_id,
        'filename_search': filename_search,
        'is_owner': is_owner,
        'highlighted_dataset_files': highlighted_dsf_pks,
        'has_write_permissions': has_write_permissions,
        'search_query' : query,
        'params' : params

        })

# microtardis change start
    if request.session['session_show_hidden']:
        # show all objects
        # highlight hidden objects
        hidden_datafiles = Datafile_Hidden.objects.filter(hidden=True).values_list('datafile', flat=True)
        objects = Dataset_File.objects.filter(dataset__pk=dataset_id, pk__in=hidden_datafiles)
        c['linethrough_dataset_files'] = [ obj.pk for obj in objects ]
# microtardis change end

    return HttpResponse(render_response_index(request, template_name, c))



def write_thumbnails(datafile, img):
    basepath = settings.THUMBNAILS_PATH
    if not os.path.exists(basepath):
        os.makedirs(basepath)
    
    # [ThumbSize, Extenstion]
    thumbnails = [(None,       ".jpg"),
                  ((400, 400), "_small.jpg")
                  ]
    
    for thumb in thumbnails:
        size = thumb[0]
        extention = thumb[1]
        if size: # None for creating thumbnail with original size
            img.thumbnail( size, Image.ANTIALIAS )
        if img.mode != "L": 
            # "L": 8-bit grayscale TIFF images, PIL can process it without problem.
            # "I;16": 16-bit grayscale TIFF images, need conversion before processing it.
            img = img.convert('I')
            table=[ i/256 for i in range(65536) ]
            img = img.point(table, 'L')
        thumbname = str(datafile.id) + extention
        thumbpath = os.path.join(basepath, thumbname)
        out = file(thumbpath, "w")
        try:
            img.save(out, "JPEG")
        finally:
            out.close()
        
def display_thumbnails(request, size, datafile_id):
    basepath = settings.THUMBNAILS_PATH
    datafile = Dataset_File.objects.get(pk=datafile_id)
    extention = ".jpg"
    if size == 'small':
        extention = "_small.jpg"
    thumbname = str(datafile.id) + extention
    thumbpath = os.path.join(basepath, thumbname)
    image_data = open(thumbpath, "rb").read()

    return HttpResponse(image_data, mimetype="image/jpeg")

def direct_to_thumbnail_html(request, datafile_id, datafile_type):
    return render_to_response("microtardis/thumbnail.html", {"datafile_id": datafile_id,
                                                 "datafile_type": datafile_type,})

def get_spc_spectra(datafile):
    basepath = settings.FILE_STORE_PATH
    experiment_id = str(datafile.dataset.experiment.id)
    dataset_id = str(datafile.dataset.id)
    raw_path = datafile.url.partition('//')[2]
    file_path = os.path.join(basepath,
                            experiment_id,
                            dataset_id,
                            raw_path)
    spc = open(file_path)
    offset = 3840
    channel = 4000 # number of spectral channels
    format = 'i' # long integer
    byte_size = 4
    
    spc.seek(offset)
    values_tuple = struct.unpack(format * channel, spc.read(byte_size * channel))
    
    return values_tuple

def get_spt_spectra(datafile):
    basepath = settings.FILE_STORE_PATH
    experiment_id = str(datafile.dataset.experiment.id)
    dataset_id = str(datafile.dataset.id)
    raw_path = datafile.url.partition('//')[2]
    file_path = os.path.join(basepath,
                            experiment_id,
                            dataset_id,
                            raw_path)
    spc = open(file_path)
    offset = 7
    channel = 2048 # number of spectral channels
    format = 'i' # long integer
    byte_size = 4
    
    spc.seek(offset)
    values_tuple = struct.unpack(format * channel, spc.read(byte_size * channel))
    
    return values_tuple

def get_spectra_csv(request, datafile_id):
    datafile = Dataset_File.objects.get(pk=datafile_id)
    filename = str(datafile.url).split('/')[-1][:-4].replace(' ', '_')
    extension = str(datafile.url)[-4:]
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % filename
    writer = csv.writer(response)
    if extension == '.spc':
        values = get_spc_spectra(datafile)
        index = 0
        for value in values:
            index += 1
            row = [index, value]
            writer.writerow(row)
    elif extension == '.spt':
        values = get_spt_spectra(datafile)
        index = 0
        for value in values:
            row = [index*10, value]
            writer.writerow(row)
            index += 1

    return response

# this function is obsolete. It's no longer to be used by javascript codes.
def get_spectra_json(request, datafile_id):
    datafile = Dataset_File.objects.get(pk=datafile_id)
    filename = str(datafile.url).split('/')[-1][:-4].replace(' ', '_')
    values = get_spc_spectra(datafile)
    index = 0
    data = []
    for value in values:
        data.append([index, value])
        index += 1
    content = '{"label": "%s", "data": %s}' % (filename, json.dumps(data))
    response = HttpResponse(content, mimetype='application/json')
    
    return response

def get_spectra_png(request, size, datafile_id, datafile_type):
    if is_matplotlib_imported:
        datafile = Dataset_File.objects.get(pk=datafile_id)
        if datafile_type == 'spc':
            values = list( get_spc_spectra(datafile) )
        elif datafile_type == 'spt':
            values = list( get_spt_spectra(datafile) )
        # truncate the values on x axis
        nonzero_values = numpy.nonzero(values)
        for i in range(0, len(nonzero_values[0])+1, 1):
            if values[nonzero_values[0][i]] < 10:
                continue
            else:
                left_end = nonzero_values[0][i]
                break
        for i in range(-1, 0-len(nonzero_values[0])+1, -1):
            if values[nonzero_values[0][i]] < 10:
                continue
            else:
                right_end = nonzero_values[0][i]
                break
        values = values[left_end:right_end+1]
        pyplot.plot([x * 0.01 for x in range(left_end, right_end+1)], values)
        
        #pyplot.plot([x * 0.01 for x in range(0, 4000)], values)
        pyplot.xlabel("keV")
        pyplot.ylabel("Counts")
        pyplot.grid(True)
        
        # set size
        ratio = 1.5
        if size == "small":
            ratio = 0.75
        fig = pyplot.gcf()
        default_size = fig.get_size_inches()
        fig.set_size_inches(default_size[0] * ratio, default_size[1] * ratio)
        
        # label peak values
        datafileparametersets = DatafileParameterSet.objects.filter(dataset_file__pk=datafile_id)
        peaks = []
        label = {}
        for parameterset in datafileparametersets:
            # get list of parameters
            parameters = parameterset.datafileparameter_set.all()
            for parameter in parameters:
                if str(parameter.name.full_name).startswith("Peak ID Element"):
                    peaks.append(parameter.string_value)
        for peak in peaks:
            data = str(peak).split(', ')
            atomic = data[0].split('=')[-1]
            line = data[1].split('=')[-1]
            energy = float(data[2].split('=')[-1])
            height= int(data[3].split('=')[-1])
            pyplot.annotate('%s%s' % (atomic, line), 
                            xy=(energy, height), 
                            xytext=(energy-0.5, height+50),
                            )
        
        # Write PNG image
        buffer = StringIO.StringIO()
        canvas = pyplot.get_current_fig_manager().canvas
        canvas.draw()
        img = Image.fromstring('RGB', canvas.get_width_height(), canvas.tostring_rgb())
        img.save(buffer, 'PNG')
        pyplot.close()
        # Django's HttpResponse reads the buffer and extracts the image
        return HttpResponse(buffer.getvalue(), mimetype='image/png')
    
    else:
        buffer = StringIO.StringIO()
        return HttpResponse(buffer.getvalue(), mimetype='image/png')
    
def hide_objects(request):
    expid = request.POST['expid']
    datasets = []
    if 'dataset' in request.POST:
        datasets = request.POST.getlist('dataset')
        for dataset in datasets:
            Dataset_Hidden.objects.filter(dataset=dataset).update(hidden=True)
            for datafile in Dataset_File.objects.filter(dataset=dataset):
                if authz.has_datafile_access(request, datafile.id):
                    Datafile_Hidden.objects.filter(datafile=datafile.id).update(hidden=True)

    if 'datafile' in request.POST:
        datafiles = request.POST.getlist('datafile')
        for datafile in datafiles:
            datafile = Dataset_File.objects.get(pk=datafile)
            if datafile.dataset.id in datasets:
                continue
            if authz.has_datafile_access(request, datafile.id):
                Datafile_Hidden.objects.filter(datafile=datafile.id).update(hidden=True)
                
    return HttpResponseRedirect(reverse('tardis.tardis_portal.views.view_experiment', args=(expid,)))

def unhide_objects(request):
    expid = request.POST['expid']
    datasets = []
    if 'dataset' in request.POST:
        datasets = request.POST.getlist('dataset')
        for dataset in datasets:
            Dataset_Hidden.objects.filter(dataset=dataset).update(hidden=False)
            for datafile in Dataset_File.objects.filter(dataset=dataset):
                if authz.has_datafile_access(request, datafile.id):
                    Datafile_Hidden.objects.filter(datafile=datafile.id).update(hidden=False)

    if 'datafile' in request.POST:
        datafiles = request.POST.getlist('datafile')
        for datafile in datafiles:
            datafile = Dataset_File.objects.get(pk=datafile)
            if datafile.dataset.id in datasets:
                continue
            if authz.has_datafile_access(request, datafile.id):
                Datafile_Hidden.objects.filter(datafile=datafile.id).update(hidden=False)
                
    return HttpResponseRedirect(reverse('tardis.tardis_portal.views.view_experiment', args=(expid,)))
