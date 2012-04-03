
MicroTardis: Customisation of MyTardis for RMIT Microscopy and Microanalysis Facility.
======================================================================================

MyTARDIS is a multi-institutional collaborative venture that
facilitates the archiving and sharing of data and metadata collected
at major facilities such as the Australian Synchrotron and ANSTO and
within Institutions.

MicroTardis is an extension of the MyTARDIS system for the task 
of transferring data and metadata from remote microscopy facilities, 
automatic extraction of microscopy image or spectra metadata, and
curation of experiments for researcher access.

Documentation
-------------

Installation, User and Developer Manuals are available at http://microtardis.readthedocs.org


Installation
------------

Get the latest version of MyTardis::

  git clone https://github.com/mytardis/mytardis.git

Install and configure mytardis based on instructions at http://mytardis.readthedocs.org/en/latest/install.html
  
Install MicroTardis extensions::

  cd mytardis/tardis
  git clone https://github.com/mytardis/microtardis.git
  
If this worked then the ``microtardis`` directory should be a the same level as the ``tardis_portal`` directory.

The file ``microtardis/test_settings_microtardis.py`` is an alternative ``tardis/test_settings.py`` for MyTardis that includes support for MicroTardis extensions

The file ``microtardis/settings_microtardis.py`` is an example ``tardis/settings_changeme.py`` for MyTardis that includes support for MicroTardis extensions