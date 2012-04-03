MicroTardis Development Guide
=============================

This document describes the architecture and implementation of the HPCTardis/MyTardis system.
The documentation includes two main parts: the first describes the features of the HPCTardis system
for curation of high performance computing datasets; and the second describes the myTardis system on which it
is built.

.. toctree::
   :maxdepth: 2




To configure HPCTardis for interactive use, modify the file ``bin/django`` and replace::

    djangorecipe.manage.main('tardis.test_settings')
    
with::
    
    djangorecipe.manage.main('tardis.settings')
    
This means that the ``bin/django`` command will run the interactive configuration rather than the test configuration.


Setup database and initial data::

    bin/django syncdb --noinput --migrate 
    
Create admin user::
    
    bin/django createsuperuser
    
Start the development server::

    bin/django runserver

System should now be running at http://127.0.0.1:8000


Testing
-------
The file ``microtardis/test_settings_microtardis.py`` is an alternative ``tardis/test_settings.py`` for MyTardis that includes support for MicroTardis extensions.

Copy ``microtardis/test_settings_microtardis.py`` into the directory in which
the ``tardis/test_settings.py`` is::

   $ cd mytardis
   $ cp tardis/microtardis/test_settings_microtardis.py tardis/test_settings_microtardis.py

    
Run testcases to verify success::

    $ cd mytardis  
    $ ./bin/django test --settings=tardis.test_settings_microtardis
    
