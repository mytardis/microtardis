MicroTardis Development Guide
=============================

This document describes information for MicroTardis developers.


Communication
-------------
The `microtardis <microtardis@googlegroups.com>`_ email list is used for 
communication between developers. To join this list, fill in the form on the 
`Contact owner to join <http://groups.google.com/group/microtardis/post?sendowner=1>`_ page.


Software Repository
-------------------
The GitHub service is used for the software repository and can be browsed using 
the `GitHub Source-code Browser <https://github.com/mytardis/microtardis>`_. 
For write access to the repository, email the `microtardis <microtardis@googlegroups.com>`_ 
list. The software can be checked out with the following command::

    git clone https://username@github.com/mytardis/mytardis.git

For anonymous checkouts the following command can be used::

    git clone https://github.com/mytardis/mytardis.git

Get the release branch you want to check out. Release branches could be: 
*2.5.0-rc1*, *mecat-ansto-dec2011*, *mecat-as-dec2011*, etc. Example::

      cd mytardis
      git tag -l
      git checkout 2.5.0-rc1


Installation
------------
1. Prerequisites

   * Redhat::

      yum install git gcc gcc-c++ httpd mod_wsgi mysql mysql-server MySQL-python 
      yum install python python-devel python-setuptools libjpeg-devel numpy python-matplotlib
      yum install cyrus-sasl-ldap cyrus-sasl-devel openldap-devel libxslt libxslt-devel libxslt-python
      easy_install PIL

   * Debian/Ubuntu::

      apt-get install git gcc libapache2-mod-wsgi mysql mysql-server python-mysqldb 
      apt-get instlal python python-dev python-setuptools python-numpy python-matplotlib
      apt-get install libpq-dev libssl-dev libsasl2-dev libldap2-dev libxslt1.1 libxslt1-dev python-libxslt1 libexiv2-dev
      easy_install PIL
      
      
2. Set RMIT Proxy
      
   If you would like to install MicroTardis in a RMIT machine, it's needed to have RMIT HTTP/HTTPS proxy settings to access the Internet. 
   
   * Copy the following lines into ``/env/environment`` with root permission to have system-wide proxy settings::
   
      HTTP_PROXY=http://bproxy.rmit.edu.au:8080
      http_proxy=http://bproxy.rmit.edu.au:8080
      HTTPS_PROXY=http://bproxy.rmit.edu.au:8080
      https_proxy=http://bproxy.rmit.edu.au:8080   
   
   * Save the file and re-login. 
   * To make sure the setting is there by opening a terminal and issuing the command::

      export | grep -i proxy
   
3. Download MyTardis and MicroTardis Extensions
   
   * Install MyTardis in the folder of your choice. Example::
   
      mkdir ~/test

   * Check out MyTardis Source Code::
   
      cd ~/test
      git clone https://github.com/mytardis/mytardis.git

   * Check out MicroTardis Extensions::
   
      cd ~/test/mytardis/tardis
      git clone https://github.com/mytardis/microtardis.git
      
4. Building
      
   MicroTardis/MyTardis is using the Buildout build system to handle the installation of dependencies and create the python class path.
   
   * Run the Buildout bootstrap script to initialise Buildout::

      cd ~/test/mytardis
      python bootstrap.py
      
   * Download and build Django and all dependencies::
      
      cd ~/test/mytardis
      bin/buildout
      
     This can be run again at any time to check for and download any new dependencies. If you get an error from getting distribution for 'coverage==3.4'. Please replace the following line in *eggs* directive under *buildout* section in ``~/test/mytardis/buildout.cfg`` file::

      coverage==3.4

     with::

      coverage  
      
      
Configuration
-------------
Configuring MicroTardis/MyTardis is done through a standard Django 
*settings.py* file. MyTardis comes with a sample configuration file at 
``~/test/mytardis/tardis/settings_changeme.py``. The file 
``~/test/mytardis/tardis/microtardis/settings_microtardis.py`` is an alternative
of ``~/test/mytardis/tardis/settings_changeme.py`` for MyTardis that includes 
support for MicroTardis extensions. The following steps will lead you to have 
your own settings file for your developmnet server.

1. Copy the file ``~/test/mytardis/tardis/microtardis/settings_microtardis.py`` into the directory where ``settings_changeme.py`` is in::

      cd ~/test/mytardis/tardis
      cp microtardis/settings_microtardis.py settings.py

2. To configure MicroTardis for interactive use, modify the file ``~/test/mytardis/bin/django`` and replace::

      djangorecipe.manage.main('tardis.test_settings')
    
   with::
    
      djangorecipe.manage.main('tardis.settings')
    
   This means that the ``~/test/mytardis/bin/django`` command will run the interactive configuration rather than the test configuration.

3. To configure database for development purpose, edit the ``~/test/mytardis/tardis/settings.py`` file as shown below::

      from os import path
      
      DATABASES = {}
      DATABASES['default'] = {}
      DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
      DATABASES['default']['NAME'] = path.join(path.dirname(__file__),'microtardis.db').replace('\\','/'), 
      DATABASES['default']['HOST'] = ''
      DATABASES['default']['PORT'] = ''
      DATABASES['default']['USER'] = ''
      DATABASES['default']['PASSWORD'] = ''

4. Change the settings for location of log files in ``~/test/mytardis/tardis/settings.py`` file as shown below::

      SYSTEM_LOG_FILENAME = 'request.log'
      MODULE_LOG_FILENAME = 'tardis.log'

5. Rename ``~/test/mytardis/tardis/tardis_portal/fixtures/initial_data.json`` to ignore importing synchrotron-specific schema::

      cd ~/test/mytardis/tardis/tardis_portal/fixtures/
      mv initial_data.json initial_data.json.ignored

6. Setup database tables in the database::
       
      cd ~/test/mytardis
      bin/django syncdb --noinput --migrate 
    
7. Create an administrator account::
    
      cd ~/test/mytardis
      bin/django createsuperuser
    
8. Start the development server::

      cd ~/test/mytardis
      bin/django runserver

9. MicroTardis web portal should now be running at:

   http://127.0.0.1:8000

10. You can now log into `Django Administration Tool <https://docs.djangoproject.com/en/dev/intro/tutorial02/>`_ with the administrator account you just created to do routin database maintenance:

   http://127.0.0.1:8000/admin


Testing
-------
The file ``~/test/mytardis/tardis/microtardis/test_settings_microtardis.py`` is an alternative ``~/test/mytardis/tardis/test_settings.py`` for MyTardis that includes support for MicroTardis extensions.

1. Copy ``~/test/mytardis/tardis/microtardis/test_settings_microtardis.py`` into the directory where the ``tardis/test_settings.py`` is in::

      cd ~/test/mytardis
      cp tardis/microtardis/test_settings_microtardis.py tardis/test_settings_microtardis.py

2. Run the testcases to verify success::

      cd ~/test/mytardis  
      bin/django test --settings=tardis.test_settings_microtardis
    

Filters
-------
The **POST_SAVE_FILTERS** variable in ``~/test/mytardis/tardis/settings.py`` file 
contains a list of post-save filters that are executed when a new DataFile 
object is created and saved to the database. The MicroTardis Filters are built 
upon the Django signal infrastrcture.

1. The POST_SAVE_FILTERS variable is specified like::

      POST_SAVE_FILTERS = [
          ("tardis.microtardis.filters.exiftags.make_filter", ["MICROSCOPY_EXIF","http://exif.schema"]),
          ("tardis.microtardis.filters.spctags.make_filter", ["EDAXGenesis_SPC","http://spc.schema"]),
          ("tardis.microtardis.filters.dattags.make_filter", ["HKLEDSD_DAT","http://dat.schema"]),
      ]
2. The format they are specified in is::

      (<filter class path>, [args], {kwargs})

   Where *args* and *kwargs* are both optional.
      