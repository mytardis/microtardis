MicroTardis Development Guide
=============================

This document describes information for MicroTardis developers.


Communication
-------------
#. The `microtardis <microtardis@googlegroups.com>`_ email list is used for 
   communication between developers. To join this list, fill in the form on the 
   `Contact owner to join <http://groups.google.com/group/microtardis/post?sendowner=1>`_ 
   page.
#. Alternatively, `tardis-devel <tardis-devel@googlegroups.com>`_ email list is 
   the one you can use to contact MyTardis/MicroTardis community. New 
   contributors are welcome, however all developers should review the 
   `pull-request checklist <https://github.com/mytardis/mytardis/wiki/Pull-Request-Checklist>`_ 
   before making pull requests.


Issue Trackers
--------------
#. The main entry point for users and system administrator is 
   `microtardis <microtardis@googlegroups.com>`_ email list.
#. Defects and issues found in the MicroTardis software are tracked using the 
   `MyTardis Lighthouse <http://mytardis.lighthouseapp.com>`_ tracker.

Software Repositories
---------------------
#. The GitHub service is used for MicroTardis software repository and can be 
   browsed using the GitHub source-code browser,

   a. `MyTardis at GitHub <https://github.com/mytardis/mytardis>`_ 
   b. `MicroTardis at GitHub <https://github.com/mytardis/microtardis>`_

#. **For write access (git push permission) to the MicroTardis repository, email 
   the** `microtardis <microtardis@googlegroups.com>`_ **list.**

   If you are a contributor to MicroTardis software, please create your personal 
   account in `GitHub <https://github.com/signup/free>`_, and send your account 
   name to `microtardis <microtardis@googlegroups.com>`_ asking for pull and 
   push permissions to MicroTardis GitHub repository.

#. Check out code from GitHub

   a. MyTardis software repository

      The software can be checked out with the following command::

        git clone https://github.com/mytardis/mytardis.git

   b. MicroTardis software repository

      If you have write access to MicroTardis github repository, use the command
      below with your own username instead to check out MicroTardis source 
      codes::

        git clone https://username@github.com/mytardis/microtardis.git

      For anonymous checkouts, the following command can be used::

        git clone https://github.com/mytardis/microtardis.git

Local Development Environment Setup
-----------------------------------

#. Internet Proxy Settings if Within RMIT Network

   **Please skip this step if your development machine isn't hosted within RMIT 
   network.**
      
   If you would like to install MicroTardis in a RMIT machine, it's required to 
   have RMIT HTTP/HTTPS proxy settings to access the Internet. 
   
   * Copy the following lines into ``/etc/environment`` with root permission to 
     have system-wide proxy settings::
   
      http_proxy=http://bproxy.rmit.edu.au:8080
      https_proxy=http://bproxy.rmit.edu.au:8080   
   
   * Save the file and re-login. 
   * To make sure the setting is there by opening a terminal and issuing the 
     command::

      export | grep -i proxy

     then you should see the proxy settings as what you have just configured.

#. Prerequisites

   MicroTardis is currently only supported on RHEL and Ubuntu. The following 
   packages are essential to be system-wide installed. 

   * Redhat::

      yum install git gcc gcc-c++ httpd mod_wsgi mysql mysql-server MySQL-python 
      yum install python python-devel python-setuptools libjpeg-devel numpy python-matplotlib
      yum install cyrus-sasl-ldap cyrus-sasl-devel openldap-devel libxslt libxslt-devel libxslt-python
      easy_install PIL

   * Ubuntu::

      apt-get install git gcc libapache2-mod-wsgi mysql mysql-server python-mysqldb 
      apt-get instlal python python-dev python-setuptools python-numpy python-matplotlib
      apt-get install libpq-dev libssl-dev libsasl2-dev libldap2-dev libxslt1.1 libxslt1-dev python-libxslt1 libexiv2-dev
      easy_install PIL
      
   
#. Download MyTardis source code

   * Choose a folder to install MyTardis. For example, your home directory.
   * Check out latest version of MyTardis Source Code::
   
      cd ~
      git clone https://github.com/mytardis/mytardis.git

#. Download MicroTardis extensions
   
   * Check out latest version of MicroTardis Extensions::
   
      cd ~/mytardis/tardis
      git clone https://github.com/mytardis/microtardis.git
      
     Please note that it is essential to check out ``microtardis`` source codes 
     into ``/opt/mytardis/tardis`` directory where the ``tardis_portal`` 
     directory is. The tardis_portal directory contains main functions of 
     MyTardis. It is necessary for MicroTardis to live in the same location of 
     it to reuse or override its features.
     
#. Use **Buildout** to set up a development environment 
      
   MicroTardis/MyTardis uses the Buildout Python-based build system to 
   automatically create, assemble and deploy applications or modules required 
   by MicroTardis/MyTardis project to build a local development environment. It 
   would automatically download and install the modules and their dependencies
   inside ``/opt/mytardis`` directory. Please note that this is not a 
   system-wide installation. Buildout uses a Python tool called setuptools 
   internally to install the packages. 
   
   * Run the **bootstrap** script to bootstrap a buildout-based project::
   
      cd ~/mytardis
      python bootstrap.py
      
   * Run the **buildout** script to download and install Python eggs and all 
     dependencies::
      
      cd ~/mytardis
      bin/buildout
      
     *This can be run again at any time to check for and download any new 
     dependencies.*
      
#. Create settings.py file

   Configuring MicroTardis/MyTardis is done through a standard Django 
   *settings.py* file. MyTardis comes with a sample configuration file at 
   ``~/mytardis/tardis/settings_changeme.py``. In MicroTardis, there is also a 
   settings file called ``~/mytardis/tardis/microtardis/settings_microtardis.py`` 
   which is an extension of ``~/mytardis/tardis/settings_changeme.py`` that 
   includes support to MicroTardis application. 
   
   To create a settings.py file in your developmnet server, just copy the file 
   ``~/mytardis/tardis/microtardis/settings_microtardis.py`` into the directory 
   where ``settings_changeme.py`` is in::

      cp ~/mytardis/tardis/microtardis/settings_microtardis.py ~/mytardis/tardis/settings.py

#. To configure MicroTardis for interactive use to proceed following parts of
   configuration, please edit the file ``~/mytardis/bin/django`` and replace the
   following line::

      djangorecipe.manage.main('tardis.test_settings')
    
   with::
    
      djangorecipe.manage.main('tardis.settings')
    
   This means that the ``~/mytardis/bin/django`` command will run the 
   interactive configuration rather than the test configuration. And we will use
   this command later on to manually create database tables or superuser, and so 
   on.

#. To configure database for development purpose, edit the database settings 
   in ``~/mytardis/tardis/settings.py`` file which you have just created as 
   shown below::

      DATABASES = {}
      DATABASES['default'] = {}
      DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
      DATABASES['default']['HOST'] = ''
      DATABASES['default']['PORT'] = ''
      DATABASES['default']['NAME'] = path.join(path.dirname(__file__),'microtardis.db').replace('\\','/'),
      DATABASES['default']['USER'] = ''
      DATABASES['default']['PASSWORD'] = ''

#. Rename ``~/mytardis/tardis/tardis_portal/fixtures/initial_data.json`` to 
   ignore importing synchrotron-specific metadata schema::

      cd ~/mytardis/tardis/tardis_portal/fixtures/
      mv initial_data.json initial_data.json.ignored

   The synchrotron-specific metadata schema is part of default schema in 
   MyTardis 2.5 release branch. However MicroTardis doesn't use it for 
   microscopy metadata data. 

#. Setup database tables in the SQLite database::
       
      cd ~/mytardis
      bin/django syncdb --noinput --migrate 
    
#. Create an administrator account::
    
      cd ~/mytardis
      bin/django createsuperuser
      
   Please keep your user name and password. You will need them to sign in 
   MicroTardis administrator web interface.
    
#. Setup MicroTardis staging area and data store

   In MyTardis/MicroTardis, **staging area** is an intermediate data storage 
   area between the sources of raw data and the MyTardis/MicroTardis 
   **data store**. It is used for gathering data from different sources that 
   will be ready to ingest into MyTardis/MicroTardis data store at different 
   times. 


   The default location of staging area or data store is in ``mytardis/var``. If 
   you have followed the installation instructions above, you should be able to 
   see them:: 

     ls -dl ~/mytardis/var/staging
     ls -dl ~/mytardis/var/store
   
   You might have noticed that both of them are empty directories. In 
   MicroTardis, data store is a file storage to keep ingested files with it 
   specific file directory structure. In this part you are not expected to 
   change or modify any data in MicroTardis data store including files and 
   directories.
   
   However, you are required to manually create a **staging structure** in
   MicroTardis staging area. Again, it needs a specific folder structure inside 
   staging to enable data ingestion from staging area into data store and 
   metadata extraction using predefined microcope-specific data filters. Please 
   follow the short instructions below to create the staging area structure for 
   your deployment.
   
   a. The first thing to do is to create **user folders** inside your staging 
      area::

        cd ~/mytardis/var/staging
        mkdir your_username
      
      You can use the administrator account that you've just created.
      
   b. Then create **microscope folders** inside user folders with any name of 
      microscope which is currently supported in MicroTardis: XL30, NovaNanoSEM,
      and Quanta200. For example::
      
        cd ~/mytardis/var/staging/your_username
        mkdir NovaNanoSEM
      
   MicroTardis currently only supports the following microscopes,
   
      * Philips XL30 SEM (1999) with Oxford Si(Li) X-ray detector and HKL EDSD 
        system
      * FEI Nova NanoSEM (2007) with EDAX Si(Li) X-ray detector
      * FEI Quanta 200 ESEM with EDAX Si(Li) X-ray detector and Gatan Alto Cyro 
        stage 

#. Copy example files into your microscope folders. Here are some example files 
   for you to download for the purpose of testing,
   
   a. XL30
   
    * `XL30.dat <_static/XL30.dat>`_
    * `XL30.spt <_static/XL30.spt>`_
    * `XL30.tif <_static/XL30.tif>`_
      
   b. NovaNanoSEM
   
    * `NovaNanoSEM.spc <_static/NovaNanoSEM.spc>`_
    * `NovaNanoSEM.tif <_static/NovaNanoSEM.tif>`_
     
   c. Quanta200 
   
    * `Quanta200.spc <_static/Quanta200.spc>`_
    * `Quanta200.tif <_static/Quanta200.tif>`_

   Download them into microscope folders according to different microscopes.
   
   Then you will be able to see the folders/files you've just created/downloaded
   on `MicroTardis Create Experiment <http://127.0.0.1:8000/experiment/create/>`_ 
   web interface later after you successfully start your development server.
    
#. Start the development server::

      cd ~/mytardis
      bin/django runserver

#. MicroTardis web portal should now be running at:

   http://127.0.0.1:8000

#. You can now log into `Django Administration Tool <https://docs.djangoproject.com/en/dev/intro/tutorial02/>`_ 
   with the administrator account you just created to do routin database maintenance:

   http://127.0.0.1:8000/admin


Testing
-------
The file ``~/mytardis/tardis/microtardis/test_settings_microtardis.py`` is an 
alternative ``~/mytardis/tardis/test_settings.py`` for MyTardis that includes 
support for MicroTardis extensions for testing purpose.

1. Copy ``~/mytardis/tardis/microtardis/test_settings_microtardis.py`` into the 
   directory where the ``tardis/test_settings.py`` is in::

      cd ~/mytardis
      cp tardis/microtardis/test_settings_microtardis.py tardis/test_settings_microtardis.py

2. Run the testcases to verify success::

      cd ~/mytardis  
      bin/django test --settings=tardis.test_settings_microtardis
    

Filters
-------
The **POST_SAVE_FILTERS** variable in ``~/mytardis/tardis/microtardis/settings_microtardis.py`` 
file contains a list of post-save filters that are executed when a new DataFile 
object is created and saved to the database. The MicroTardis Filters are built 
upon the Django signal infrastrcture.

1. The POST_SAVE_FILTERS variable in settings file is specified like::

      POST_SAVE_FILTERS = [
          ("tardis.microtardis.filters.exiftags.make_filter", ["MICROSCOPY_EXIF","http://exif.schema"]),
          ("tardis.microtardis.filters.spctags.make_filter", ["EDAXGenesis_SPC","http://spc.schema"]),
          ("tardis.microtardis.filters.dattags.make_filter", ["HKLEDSD_DAT","http://dat.schema"]),
      ]
2. The format they are specified in is::

      (<filter class path>, [args], {kwargs})

   Where *args* and *kwargs* are both optional.
      
3. In MicroTardis, filters are in charge of creating microscope metadata schemas
   in database on the fly and extracting metadata from raw data files and saving
   metadata into database. 
   
   In terms of spectra values extraction, MicroTardis doesn't store those values
   in database but keep them in spectrum files instead. It has a function called
   *get_spectra_csv* in ``microtardis/views.py`` in charge of extracting spectra
   values from spectrum files (.spt or .spc) on the fly as users request to 
   download them in CSV file format from web portal interface.
   
   Currently we have the following filters implemented,      
      
   +---------------------+----------------+------------------+-------------+-----------------+---------------------------+
   | Microscope          | Detector       | Analysis System  | File        | Filter or       | Description               |
   |                     |                |                  | Extension   | Function        |                           |
   +=====================+================+==================+=============+=================+===========================+
   | Philips XL30 SEM    | Oxford Si(Li)  | Moran Scientific | .tif        | exiftags.py     | extract image metadata    |
   |                     | X-ray detector |                  +-------------+-----------------+---------------------------+
   |                     | and HKL EDSD   |                  | .spt        | get_spectra_csv | extract spectra values    |
   |                     | system         |                  |             | in views.py     | (in CSV format)           |
   |                     |                |                  +-------------+-----------------+---------------------------+
   |                     |                |                  | .dat        | dattags.py      | extract spectrum metadata |
   +---------------------+----------------+------------------+-------------+-----------------+---------------------------+
   | FEI Nova NanoSEM    | EDAX Si(Li)    | EDAX Genesis     | .tif        | exiftags.py     | extract image metadata    |
   |                     | X-ray detector |                  +-------------+-----------------+---------------------------+
   |                     |                |                  | .spc        | spctags.py      | extract spectrum metadata |
   |                     |                |                  |             +-----------------+---------------------------+
   |                     |                |                  |             | get_spectra_csv | extract spectra values    |
   |                     |                |                  |             | in views.py     | (in CSV format)           |
   +---------------------+----------------+------------------+-------------+-----------------+---------------------------+
   | FEI Quanta 200 ESEM | EDAX Si(Li)    | EDAX Genesis     | .tif        | exiftags.py     | extract image metadata    |
   |                     | X-ray detector |                  +-------------+-----------------+---------------------------+
   |                     | and Gatan Alto |                  | .spc        | spctags.py      | extract spectrum metadata |
   |                     | Cyro stage     |                  |             +-----------------+---------------------------+
   |                     |                |                  |             | get_spectra_csv | extract spectra values    |
   |                     |                |                  |             | in views.py     | (in CSV format)           |
   +---------------------+----------------+------------------+-------------+-----------------+---------------------------+
      
User Registration
-----------------

MicroTardis has two authentication methods. One is **local** user authentication 
which is the default solution using a local authentication database. In this 
case, site administrator is required to perform user account maintenance and 
validation tasks. For each valid user, site administrator has to manually create
a user account with a username and a password and grant this user proper 
privileges to register he/she in MicroTardis. For a quick guide to create user 
account, please see `MicroTardis Administration Guide <http://readthedocs.org/docs/microtardis/en/latest/microtardis_administration.html>`_.

The other method is **integrated** user authentication with 
`RMMF Booking System (EMBS) <http://embs.set.rmit.edu.au/mebookings.php>`_ which
uses a remote RMMF authentication database. MicroTardis site administrator is 
not required to maintain user accounts in MicroTardis database in this case. It
automatically creates a new user account in MicroTardis local authentication 
database when a valid RMMF user (who has registered as an user in EMBS) first 
log in MicroTardis with a valid username and a valid password. In this case, the
first login is considered as user registration in MicroTardis. After successful 
registration, MicroTardis would only use local authentication database to 
authenticate users. There won't be communication between MicroTardis and EMBS
for user authentication if the user account already exists in MicroTardis 
database.