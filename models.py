from django.db import models
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

from tardis.tardis_portal.models import Experiment
from tardis.tardis_portal.models import Dataset
from tardis.tardis_portal.models import Dataset_File

#-------------------
# Experiment Hidden
#-------------------
class Experiment_Hidden(models.Model):
    experiment = models.ForeignKey(Experiment)
    hidden = models.BooleanField(default=False)

@receiver(post_save, sender=Experiment)
def save_experiment_hidden(sender, instance, created, **kwargs):
    if created:
        Experiment_Hidden.objects.get_or_create(experiment=instance)
        
@receiver(post_delete, sender=Experiment)
def delete_experiment_hidden(sender, instance, **kwargs):
    try:
        object = Experiment_Hidden.objects.get(experiment=instance)
        object.delete()
    except Experiment_Hidden.DoesNotExist:
        pass 

#-------------------
# Dataset Hidden
#-------------------
class Dataset_Hidden(models.Model):
    dataset = models.ForeignKey(Dataset) 
    hidden = models.BooleanField(default=False)

@receiver(post_save, sender=Dataset)  
def save_dataset_hidden(sender, instance, created, **kwargs):
    if created:
        Dataset_Hidden.objects.get_or_create(dataset=instance)

@receiver(post_delete, sender=Dataset)
def delete_dataset_hidden(sender, instance, **kwargs):
    try:
        object = Dataset_Hidden.objects.get(dataset=instance)
        object.delete()
    except Dataset_Hidden.DoesNotExist:
        pass  
 
#-------------------
# Datafile Hidden
#-------------------    
class Datafile_Hidden(models.Model):
    datafile = models.ForeignKey(Dataset_File) 
    hidden = models.BooleanField(default=False)    

@receiver(post_save, sender=Dataset_File)
def save_datafile_hidden(sender, instance, created, **kwargs):
    if created:
        Datafile_Hidden.objects.get_or_create(datafile=instance)

@receiver(post_delete, sender=Dataset_File)
def delete_datafile_hidden(sender, instance, **kwargs):
    try:
        object = Datafile_Hidden.objects.get(datafile=instance)
        object.delete()
    except Datafile_Hidden.DoesNotExist:
        pass  
    
#-------------------
# Dataset Harvest
#-------------------    
class Dataset_Harvest(models.Model):
    dataset = models.ForeignKey(Dataset) 
    created_time = models.DateTimeField(auto_now_add=True)
    instrument = models.CharField(max_length=80)

@receiver(post_save, sender=Dataset)
def save_dataset_harvest(sender, instance, created, **kwargs):
    instrument = ""
    if created:
        Dataset_Harvest.objects.get_or_create(dataset=instance, instrument=instrument)

@receiver(post_delete, sender=Dataset)
def delete_dataset_harvest(sender, instance, **kwargs):
    try:
        object = Dataset_Harvest.objects.get(dataset=instance)
        object.delete()
    except Dataset_Harvest.DoesNotExist:
        pass  

#-------------------
# Datafile Harvest
#-------------------    
class Datafile_Harvest(models.Model):
    datafile = models.ForeignKey(Dataset_File) 
    created_time = models.DateTimeField(auto_now_add=True)
    instrument = models.CharField(max_length=80)

@receiver(post_save, sender=Dataset_File)
def save_datafile_harvest(sender, instance, created, **kwargs):
    if created:
        instrument = ""
        url = str(instance.url)
        if url.startswith('tardis://'):
            instrument = url.split('/')[2]
        Datafile_Harvest.objects.get_or_create(datafile=instance, instrument=instrument)

@receiver(post_delete, sender=Dataset_File)
def delete_datafile_harvest(sender, instance, **kwargs):
    try:
        object = Datafile_Harvest.objects.get(datafile=instance)
        object.delete()
    except Datafile_Harvest.DoesNotExist:
        pass