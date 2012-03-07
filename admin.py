from django.contrib import admin

from tardis.apps.microtardis.models import Experiment_Hidden
from tardis.apps.microtardis.models import Dataset_Hidden
from tardis.apps.microtardis.models import Datafile_Hidden
from tardis.apps.microtardis.models import Dataset_Harvest
from tardis.apps.microtardis.models import Datafile_Harvest

class Experiment_Hidden_Admin(admin.ModelAdmin):
    list_display = ('experiment', 'hidden',)
    ordering = ('id',)
    list_filter = ('hidden',)

admin.site.register(Experiment_Hidden, Experiment_Hidden_Admin)

class Dataset_Hidden_Admin(admin.ModelAdmin):
    list_display = ('dataset', 'hidden',)
    ordering = ('id',)
    list_filter = ('hidden',)

admin.site.register(Dataset_Hidden, Dataset_Hidden_Admin)

class Datafile_Hidden_Admin(admin.ModelAdmin):
    list_display = ('datafile', 'hidden',)
    ordering = ('id',)
    list_filter = ('hidden',)

admin.site.register(Datafile_Hidden, Datafile_Hidden_Admin)

class Dataset_Harvest_Admin(admin.ModelAdmin):
    list_display = ('dataset', 'created_time', 'instrument',)
    ordering = ('id',)
    list_filter = ('instrument',)

admin.site.register(Dataset_Harvest, Dataset_Harvest_Admin)

class Datafile_Harvest_Admin(admin.ModelAdmin):
    list_display = ('datafile', 'created_time', 'instrument',)
    ordering = ('id',)
    list_filter = ('instrument',)

admin.site.register(Datafile_Harvest, Datafile_Harvest_Admin)