# -*- coding: utf-8 -*-
#
# Copyright (c) 2011-2011, RMIT e-Research Office
#   (RMIT University, Australia)
# Copyright (c) 2010-2011, Monash e-Research Centre
#   (Monash University, Australia)
# Copyright (c) 2010-2011, VeRSI Consortium
#   (Victorian eResearch Strategic Initiative, Australia)
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    *  Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    *  Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#    *  Neither the name of the VeRSI, the VeRSI Consortium members, nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

"""
dattags.py

.. moduleauthor:: Russell Sim <russell.sim@monash.edu>
.. moduleauthor:: Joanna H. Huang <Joanna.Huang@versi.edu.au>

"""

from tardis.tardis_portal.models import Schema, DatafileParameterSet
from tardis.tardis_portal.models import ParameterName, DatafileParameter
from tardis.tardis_portal.models import DatasetParameter
import logging
import string
import csv

from django.conf import settings


logger = logging.getLogger(__name__)

class DATTagsFilter(object):
    """This filter provides extraction of metadata extraction of 
    HKL EDSD spectral metadata files (*.dat) from the RMMF.

    If a white list is specified then it takes precedence and all
    other tags will be ignored.

    :param name: the short name of the schema.
    :type name: string
    :param schema: the name of the schema to load the meta data into.
    :type schema: string
    :param tagsToFind: a list of the tags to include.
    :type tagsToFind: list of strings
    :param tagsToExclude: a list of the tags to exclude.
    :type tagsToExclude: list of strings
    """
    def __init__(self, name, schema, tagsToFind=[], tagsToExclude=[]):
        self.name = name
        self.schema = schema
        self.tagsToFind = tagsToFind
        self.tagsToExclude = tagsToExclude
        
        self.instruments = {'XL30': (('HKLEDSD_DAT', 'HKLEDSD_DAT', None),),
                            }
        logger.debug('initialising DATTagsFilter')

    def __call__(self, sender, **kwargs):
        """post save callback entry point.

        :param sender: The model class.
        :param instance: The actual instance being saved.
        :param created: A boolean; True if a new record was created.
        :type created: bool
        """
        instance = kwargs.get('instance')
        created = kwargs.get('created')
#        if not created:
#            # Don't extract on edit
#            return
#        #  schema = self.getSchema()
        
        filepath = instance.get_absolute_filepath()
        if not filepath:
            # TODO log that exited early
            return
        
        #ignore non-dat file
        if filepath[-4:].lower() != ".dat":
            return
        
        # Find instrument name in filepath
        instr_name = None 
        import re
        pathSep = re.compile(r'\\|\/')
        for part in pathSep.split(filepath):
            if part in self.instruments.keys():
                instr_name = part
        
        # Find instrument name in dataset metadata
        if not instr_name:
            # couldn't find it in filepath, then try dataset metadata
            dataset_params = DatasetParameter.objects.filter(parameterset__dataset__id=instance.dataset.id)
            for dataset_param in dataset_params:
                str_value = str(dataset_param.string_value)
                if str_value.startswith('http://'):
                    parts = str_value.split('/')
                    if len(parts) > 4:
                        instr_name = parts[4]
                else:
                    continue

        logger.debug("filepath=%s" % filepath)
        logger.debug("instr_name=%s" % instr_name)

        if (instr_name != None and len(instr_name) > 1):
            
            # get spectral metadata 
            metadata = self.getSpectra(filepath)
        
            # get schema (create schema if needed)
            instrSchemas = self.instruments[instr_name]
            schema_name = "HKLEDSD_DAT"
            for sch in instrSchemas:
                if sch[0] == schema_name:
                    (schemaName, schemaSuffix, tagsToFind) = sch
            if not schemaName:
                logger.debug("Schema %s doesn't exist for instrument %s" % (schema_name, instr_name))
                return
            instrNamespace = ''.join([self.schema, "/" , schemaSuffix]) 
            (schema, created) = Schema.objects.get_or_create(namespace=instrNamespace, name=schemaName,type=Schema.DATAFILE)
            if created: # new object was created
                schema.save()
                
            # save spectral metadata
            self.saveSpectraMetadata(instance, schema, metadata)

    def saveSpectraMetadata(self, instance, schema, metadata):
        """Save all the metadata to a Dataset_Files paramamter set.
        """
        parameters = self.getParamaters(schema, metadata)
        if not parameters:
            return None
        
        (ps, created) = DatafileParameterSet.objects.get_or_create(schema=schema, dataset_file=instance)
        if created: # new object was created
            ps.save()
        else: # if parameter set already exists then just return it
            return ps 

        # save datafile parameters
        for p in parameters:
            if p.name in metadata:
                dfp = DatafileParameter(parameterset=ps,
                                        name=p)
                if p.isNumeric():
                    dfp.numerical_value = metadata[p.name][0]
                else:
                    dfp.string_value = metadata[p.name][0]
                dfp.save()
                
        return ps

    def getParamaters(self, schema, metadata):
        """Return a list of the paramaters that will be saved.
        """
        param_objects = ParameterName.objects.filter(schema=schema)
        parameters = []
        for p in metadata:

            if self.tagsToFind and not p in self.tagsToFind:
                continue

            if p in self.tagsToExclude:
                continue

            parameter = filter(lambda x: x.name == p, param_objects)

            if parameter:
                parameters.append(parameter[0])
                continue

            # detect type of parameter
            datatype = ParameterName.STRING
             
            # integer data type test
            try:
                int(metadata[p][0])
            except (ValueError, TypeError):
                pass
            else:
                datatype = ParameterName.NUMERIC
            
            # float data type test
            try:
                float(metadata[p][0])
            except (ValueError, TypeError):
                pass
            else:
                datatype = ParameterName.NUMERIC

            unit = ""
            if metadata[p][1]:
                unit = metadata[p][1]
      
            new_param = ParameterName(schema=schema,
                                      name=p,
                                      full_name=p,
                                      data_type=datatype,
                                      units=unit)
            new_param.save()
            parameters.append(new_param)
        return parameters

    def getSchema(self):
        """Return the schema object that the paramaterset will use.
        """
        try:
            return Schema.objects.get(namespace__exact=self.schema)
        except Schema.DoesNotExist:
            schema = Schema(namespace=self.schema, name=self.name,
                            type=Schema.DATAFILE)
            schema.save()
            return schema




    def getSpectra(self, filename):
        """Return a dictionary of the metadata.
        """
        logger.debug("Extracting spectral metadata from *.dat file...")
        ret = {}
        try:
            dat = open(filename)
            csvReader = csv.reader(dat, delimiter=',')
            value = ""
            unit = ""
            element_count = 1
            for row in csvReader:
                # Elements detected
                if len(row) == 3:
                    tmp_list = row[2].split(' ')
                    atomic_value = tmp_list[0]
                    line_value = tmp_list[1][:1] #ignore non-unicode character
                    energy_value = float(row[1])
                    height_value = int(row[0])
                    field = "Element %s" % element_count
                    value = "Atomic=%s, Line=%s, Energy=%.4f, Height=%d" % \
                            (atomic_value, line_value, energy_value, height_value)
                    ret[field] = [value, unit]
                    element_count += 1
                # Counts per second
                if row[0] == 'Cpspn':
                    field = "Counts Per Second"
                    value = float(row[1])
                    unit = ""
                    ret[field] = [value, unit]
                # Beam voltage
                if row[0] == 'KeV':
                    field = "Beam Voltage"
                    value = float(row[1])
                    unit = "kV"
                    ret[field] = [value, unit]
        except:
            #print "Failed to extract spectral metadata from *.dat file."
            import sys
            #print sys.exc_info()
            #print ret
            logger.debug("Failed to extract spectral metadata from *.dat file.")
            return ret
        
        logger.debug("Successed extracting spectral metadata from *.dat file.")
        return ret

def make_filter(name='', schema='', tagsToFind=[], tagsToExclude=[]):
    if not name:
        raise ValueError("DATTagsFilter requires a name to be specified")
    if not schema:
        raise ValueError("DATTagsFilter required a schema to be specified") 
    return DATTagsFilter(name, schema, tagsToFind, tagsToExclude)

make_filter.__doc__ = DATTagsFilter.__doc__