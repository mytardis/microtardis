.. _installation:

************************************
Installing Your MicroTardis Instance
************************************

This document describes how to install MicroTardis/MyTardis system.
The documentation includes two main parts: the first part describes the installation
of MyTardis system and MicroTardis extensions; and the second part describes 
deploying MicroTardis within RMIT ITS network.

.. _installing_microtardis:

Installing MicroTardis
======================

Step 1: Prerequisites
---------------------
MicroTardis is currently only supported on RHEL and Debian/Ubuntu with SELinux disabled.

1. Redhat::

      sudo yum install git gcc httpd mod_wsgi mysql mysql-server MySQL-python python-setuptools python-devel 
      sudo yum install cyrus-sasl-ldap cyrus-sasl-devel openldap-devel libxslt libxslt-devel libxslt-python

2. Debian/Ubuntu::

      sudo apt-get install git python-dev libpq-dev libssl-dev libsasl2-dev libldap2-dev libxslt1.1 libxslt1-dev python-libxslt1 libexiv2-dev
   
Step 2: Access the Internet via the RMIT Proxy
----------------------------------------------
If you would like to install MicroTardis in a RMIT machine, it's needed to have RMIT proxy settings to access the Internet. 

1. Copy the following lines into ``/env/environment`` with root permission to have system-wide proxy settings::
   
      HTTP_PROXY=http://bproxy.rmit.edu.au:8080
      http_proxy=http://bproxy.rmit.edu.au:8080
      HTTPS_PROXY=http://bproxy.rmit.edu.au:8080
      https_proxy=http://bproxy.rmit.edu.au:8080   
   
2. Save the file and re-login. 
3. To make sure the setting is there by opening a terminal and issuing the command::

      export | grep http_proxy
    
Step 3: Download MyTardis Source Code
-------------------------------------
1. To get the 2.5 release branch::

      git clone git://github.com/mytardis/mytardis.git
      cd mytardis
      git tag -l
      git checkout 2.5.0-rc1

2. If you get an error of connection timed out as shown below::

      Initialized empty Git repository in /dirpath/mytardis/.git/
      github.com[0: 207.97.227.239]: errno=Connection timed out
      fatal: unable to connect a socket (Connection timed out)

   Please use the following commands instead (cloning GitHub repository over HTTP)::

      git config --global http.proxy bproxy.rmit.edu.au:8080
      git clone https://github.com/mytardis/mytardis.git
      cd mytardis
      git tag -l
      git checkout 2.5.0-rc1

   It might be slow and recommended to be used if the git port(9418) is blocked due to a firewall constraint.

Step 4: Download MicroTardis Extensions
---------------------------------------
1. To get the current master branch::

      cd mytardis/tardis
      git clone https://github.com/mytardis/microtardis.git
   
   
Step 5: Building
---------------------------

MicroTardis/MyTardis is using the Buildout build system to handle the installation of dependencies and create the python class path.
   
1. Run the Buildout bootstrap script to initialise Buildout::

      cd mytardis
      python bootstrap.py
   
   If you get a Python urllib2.URLError complaining "Connection timed out", you may have Internet access blocked. Please do Step 2, or run the following commands before bootstrap::

      export HTTP_PROXY=http://bproxy.rmit.edu.au:8080
      export http_proxy=http://bproxy.rmit.edu.au:8080
      export HTTPS_PROXY=http://bproxy.rmit.edu.au:8080
      export https_proxy=http://bproxy.rmit.edu.au:8080
   
2. Download and build Django and all dependencies::

      cd mytardis
      bin/buildout
   
   This can be run again at any time to check for and download any new dependencies.   

   If you get an error from getting distribution for 'coverage==3.4'. Please replace the following line in *eggs* directive under buildout section in *buildout.cfg* file::

      coverage==3.4

   with::

      coverage
   
Deploying MicroTardis
=====================

Step 1: MicroTardis settings.py File
------------------------------------

Configuring MicroTardis/MyTardis is done through a standard Django 
*settings.py* file. MyTardis comes with a sample configuration file at 
``tardis/settings_changeme.py``. The file 
``tardis/microtardis/settings_microtardis.py`` is an example of 
``tardis/settings_changeme.py`` for MyTardis that includes support for 
MicroTardis extensions. The following steps will lead you to have your own
settings file for your deployment.

1. Copy the file ``tardis/microtardis/settings_microtardis.py`` into the directory in which ``settings_changeme.py`` is::

      cd mytardis
      cp tardis/microtardis/settings_microtardis.py tardis/settings.py

Step 2: MicroTardis Database
----------------------------
1. Ensure that the MySQL database has been started::
   
      sudo /etc/init.d/mysqld start
   
2. Configure MySQL to run every time the system starts::

      sudo chkconfig mysqld on

3. Run the following command to configure the database; don't forget to replace 'secret' with a password of your choice::

      sudo mysql -e "CREATE DATABASE microtardis"
      sudo mysql -e "GRANT ALL PRIVILEGES ON microtardis.* TO 'microtardis'@'localhost' IDENTIFIED BY 'secret';"
   
4. Edit the ``tardis/settings.py`` file and ensure that DATABASE_PASSWORD and other database parameters match the values used to create the MicroTardis database::

      DATABASES = {}
      DATABASES['default'] = {}
      DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
      DATABASES['default']['HOST'] = 'localhost'
      DATABASES['default']['PORT'] = '3306'
      DATABASES['default']['NAME'] = 'microtardis'
      DATABASES['default']['USER'] = 'microtardis'
      DATABASES['default']['PASSWORD'] = 'secret'

5. Run the following command to ensure that the MySQL instance has a root password; don't forget to replace the word 'secret' with a password of your choice::

      sudo mysqladmin password secret

   If you need to reset MySQL root password, then run the following command to reset the password of your choice::

      sudo mysqladmin -u root -pcurrentpassword password 'newpassword'

   Please note that there is no space between -p and currentpassword. Or change MySQL root password from MySQL prompt using UPDATE SQL command::

      mysql> UPDATE user SET password=PASSWORD('newpassword') WHERE user='root';
      mysql> flush privileges;
      mysql> exit;

   Once you've changed it, make sure you can login with your new password successfully. And now kill your running MySQL deamon, then restart it normally.

6. Rename ``tardis/tardis_portal/fixtures/initial_data.json`` to ignore importing synchrotron-specific metadata::

      cd mytardis/tardis/tardis_portal/fixtures/
      mv initial_data.json initial_data.json.ignored

7. To configure MicroTardis for interactive use, modify the file ``bin/django`` and replace the following line::

       djangorecipe.manage.main('tardis.test_settings')

   with::
    
       djangorecipe.manage.main('tardis.settings')
    
   This means that the ``bin/django`` command will run the interactive configuration rather than the test configuration.

8. Run the following command to setup the database tables in the database::

      cd mytardis
      bin/django syncdb --noinput --migrate 


Step 3: MicroTardis Administrator
---------------------------------
1. Create an administrator account::

      cd mytardis
      bin/django createsuperuser


Step 4: Static Files
--------------------
For performance reasons you should avoid static files being served via the 
application, and instead serve them directly through the webserver.

1. To collect all the static files to a single directory::

      cd mytardis
      bin/django collectstatic


Step 5: Apache and mod_wsgi
---------------------------
1. Create a symbolic link from MyTardis to standard ``/var/www`` structure (makes a fixed path for later changes)::

      cd /var/www
      ln -s /path/to/mytardis mytardis

2. Edit ``/etc/httpd/conf.d/wsgi.conf`` file::

      LoadModule wsgi_module modules/mod_wsgi.so
      <IfModule mod_wsgi.c>
          AddHandler wsgi-script .wsgi
          Include /var/www/mytardis/apache/apache_django_wsgi.conf
      </IfModule>
  
3. Create ``/var/www/mytardis/apache/apache_django_wsgi.conf`` file::

      cd mytardis/apache
      cp cp apache_django_wsgi.conf_changeme apache_django_wsgi.conf

4. Edit the ``/var/www/mytardis/apache/apache_django_wsgi.conf`` file as shown below::

      Alias /static/ /var/www/mytardis/static/
      <Directory /var/www/mytardis/static/>
      Order deny,allow
      Allow from all
      </Directory>
      
      WSGIScriptAlias / "/var/www/mytardis/apache/django.wsgi"
      
      <Directory "/var/www/mytardis/apache">
      Allow from all
      </Directory>

5. Create ``/var/www/mytardis/apache/django.wsgi`` file::
  
      cd mytardis/apache
      cp django.wsgi_changeme django.wsgi
  
6. Edit the ``/var/www/mytardis/apache/django.wsgi`` file as shown below (Please copy the value of *sys.path* variable from ``mytardis/bin/django`` file)::
  
      #!/usr/bin/python
      
      import os
      import sys
      sys.path[0:0] = [
          '/path/to/mytardis',
          ...
          ]
      
      os.environ['DJANGO_SETTINGS_MODULE'] = 'tardis.settings'
      import django.core.handlers.wsgi
      application = django.core.handlers.wsgi.WSGIHandler()




This is the minimum set of changes required to successfully run the server. You can make any other site-specific changes as necessary.