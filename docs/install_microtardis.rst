.. _installation:

************************************
Installing Your MicroTardis Instance
************************************

This document describes a step by step guide on how to install MicroTardis/MyTardis system.
The documentation includes two main parts: the first part describes the installation
of MyTardis system and MicroTardis extensions; and the second part describes 
deploying MicroTardis within RMIT ITS network.

.. _installing_microtardis:

Installing MicroTardis
======================

Step 1: Prerequisites
---------------------
MicroTardis is currently only supported on RHEL and Ubuntu with SELinux disabled.

**Please note that these installation instructions were written based on a RHEL 6 installation.**

1. Redhat::

      yum install git gcc gcc-c++ httpd mod_wsgi mysql mysql-server MySQL-python 
      yum install python python-devel python-setuptools libjpeg-devel numpy python-matplotlib
      yum install cyrus-sasl-ldap cyrus-sasl-devel openldap-devel libxslt libxslt-devel libxslt-python
      easy_install PIL

2. Ubuntu::

      apt-get install git gcc libapache2-mod-wsgi mysql mysql-server python-mysqldb 
      apt-get instlal python python-dev python-setuptools python-numpy python-matplotlib
      apt-get install libpq-dev libssl-dev libsasl2-dev libldap2-dev libxslt1.1 libxslt1-dev python-libxslt1 libexiv2-dev
      easy_install PIL
      
   
Step 2: Access the Internet via the RMIT Proxy
----------------------------------------------
If you would like to install MicroTardis in a RMIT machine, it's needed to have RMIT HTTP/HTTPS proxy settings to access the Internet. 

1. Copy the following lines into ``/env/environment`` with root permission to have system-wide proxy settings::
   
      HTTP_PROXY=http://bproxy.rmit.edu.au:8080
      http_proxy=http://bproxy.rmit.edu.au:8080
      HTTPS_PROXY=http://bproxy.rmit.edu.au:8080
      https_proxy=http://bproxy.rmit.edu.au:8080   
   
2. Save the file and re-login. 
3. To make sure the setting is there by opening a terminal and issuing the command::

      export | grep -i proxy
    
    
Step 3: Download MyTardis Source Code
-------------------------------------
1. Get the 2.5 release branch and check out the source code into ``/opt/`` directory::

      cd /opt
      git clone git://github.com/mytardis/mytardis.git
      cd mytardis
      git tag -l
      git checkout 2.5.0-rc1

2. If you get an error of connection timed out as shown below::

      Initialized empty Git repository in /opt/mytardis/.git/
      github.com[0: 207.97.227.239]: errno=Connection timed out
      fatal: unable to connect a socket (Connection timed out)

   Please use the following commands instead (cloning GitHub repository over HTTP)::

      cd /opt
      git config --global http.proxy bproxy.rmit.edu.au:8080
      git clone https://github.com/mytardis/mytardis.git
      cd mytardis
      git tag -l
      git checkout 2.5.0-rc1

   It might be slow and recommended to be used if the git port(9418) is blocked due to a firewall constraint.


Step 4: Download MicroTardis Extensions
---------------------------------------
1. To get the current master branch::

      cd /opt/mytardis/tardis
      git clone https://github.com/mytardis/microtardis.git
   
   
Step 5: Building
---------------------------

MicroTardis/MyTardis is using the Buildout build system to handle the installation of dependencies and create the python class path.
   
1. Run the Buildout bootstrap script to initialise Buildout::

      cd /opt/mytardis
      python bootstrap.py
   
   If you get a Python urllib2.URLError complaining "Connection timed out", you may have Internet access blocked. Please do Step 2, or run the following commands before bootstrap::

      export HTTP_PROXY=http://bproxy.rmit.edu.au:8080
      export http_proxy=http://bproxy.rmit.edu.au:8080
      export HTTPS_PROXY=http://bproxy.rmit.edu.au:8080
      export https_proxy=http://bproxy.rmit.edu.au:8080
   
2. Download and build Django and all dependencies::

      cd /opt/mytardis
      bin/buildout
   
   This can be run again at any time to check for and download any new dependencies.   

   If you get an error from getting distribution for 'coverage==3.4'. Please replace the following line in *eggs* directive under *buildout* section in ``/opt/mytardis/buildout.cfg`` file::

      coverage==3.4

   with::

      coverage
   
Deploying MicroTardis
=====================

Step 1: MicroTardis settings.py File
------------------------------------

Configuring MicroTardis/MyTardis is done through a standard Django 
*settings.py* file. MyTardis comes with a sample configuration file at 
``/opt/mytardis/tardis/settings_changeme.py``. The file 
``/opt/mytardis/tardis/microtardis/settings_microtardis.py`` is an example of 
``/opt/mytardis/tardis/settings_changeme.py`` for MyTardis that includes support for 
MicroTardis extensions. The following steps will lead you to have your own
settings file for your deployment.

1. Copy the file ``/opt/mytardis/tardis/microtardis/settings_microtardis.py`` into the directory where ``settings_changeme.py`` is in::

      cd /opt/mytardis/tardis
      cp microtardis/settings_microtardis.py settings.py


Step 2: MicroTardis Database
----------------------------
1. Ensure that the MySQL database has been started::
   
      /etc/init.d/mysqld start
   
2. Configure MySQL to run every time the system starts::

      chkconfig mysqld on

3. Run the following command to configure the database; don't forget to replace *'secret'* with a password of your choice::

      mysql -e "CREATE DATABASE microtardis"
      mysql -e "GRANT ALL PRIVILEGES ON microtardis.* TO 'microtardis'@'localhost' IDENTIFIED BY 'secret';"
   
4. Edit the ``/opt/mytardis/tardis/settings.py`` file and ensure that DATABASE_PASSWORD and other database parameters match the values used to create the MicroTardis database::

      DATABASES = {}
      DATABASES['default'] = {}
      DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
      DATABASES['default']['HOST'] = 'localhost'
      DATABASES['default']['PORT'] = '3306'
      DATABASES['default']['NAME'] = 'microtardis'
      DATABASES['default']['USER'] = 'microtardis'
      DATABASES['default']['PASSWORD'] = 'secret'
      
   This is the minimum set of changes required to successfully run the server. You can make any other site-specific changes in ``/opt/mytardis/tardis/settings.py`` as necessary.

5. Run the following command to ensure that the MySQL instance has a root password; don't forget to replace the word *'secret'* with a password of your choice::

      mysqladmin password secret

   If you need to reset MySQL root password, then run the following command to reset the password of your choice::

      mysqladmin -u root -pcurrentpassword password 'newpassword'

   Please note that there is no space between -p and currentpassword. Or change MySQL root password from MySQL prompt using UPDATE SQL command::

      mysql> UPDATE user SET password=PASSWORD('newpassword') WHERE user='root';
      mysql> FLUSH PRIVILEGES;
      mysql> EXIT;

   Once you've changed it, make sure you can login with your new password successfully. And now kill your running MySQL deamon, then restart it normally.

6. Rename ``/opt/mytardis/tardis/tardis_portal/fixtures/initial_data.json`` to ignore importing synchrotron-specific schema::

      cd /opt/mytardis/tardis/tardis_portal/fixtures/
      mv initial_data.json initial_data.json.ignored

7. To configure MicroTardis for interactive use, modify the file ``/opt/mytardis/bin/django`` and replace the following line::

       djangorecipe.manage.main('tardis.test_settings')

   with::
    
       djangorecipe.manage.main('tardis.settings')
    
   This means that the ``/opt/mytardis/bin/django`` command will run the interactive configuration rather than the test configuration.

8. Run the following command to setup the database tables in the database::

      cd /opt/mytardis
      bin/django syncdb --noinput --migrate 


Step 3: MicroTardis Administrator
---------------------------------
1. Create an administrator account::

      cd /opt/mytardis
      bin/django createsuperuser


Step 4: Static Files
--------------------
For performance reasons you should avoid static files being served via the 
application, and instead serve them directly through the webserver.

1. To collect all the static files to a single directory::

      cd /opt/mytardis
      bin/django collectstatic


Step 5: MicroTardis Staging Area and Store
------------------------------------------
If you need to use remote storage (mounted) staging/store area, please create symbolic links in ``/opt/mytardis/var`` to replace old staging and store directories.

1. Create a symbolic link for *staging* area from MicroTardis to the remote storage::

      cd /opt/mytardis/var
      rmdir staging
      ln -s /mnt/your_remote_staging staging
    
2. Create a symbolic link for *store* from MicroTardis to the remote storage::

      cd /opt/mytardis/var
      rmdir store
      ln -s /mnt/your_remote_store store

Step 6: Apache and mod_wsgi
---------------------------
1. Create a symbolic link from MyTardis to standard ``/var/www/html`` structure (makes a fixed path for later changes)::

      cd /var/www/html
      chmod o+w /var/www/html
      sudo -u apache ln -s /opt/mytardis mytardis
      chmod o-w /var/www/html
      
2. Set up a virtual host for MicroTardis web portal by editing ``/etc/httpd/conf/httpd.conf`` file::

      <VirtualHost *:80>
          ServerAdmin webmaster@localhost
          DocumentRoot /var/www/html/mytardis
          <Directory />
              Options +FollowSymLinks
              AllowOverride None
          </Directory>
          <Directory /var/www/html/mytardis>
              Options Indexes +FollowSymLinks MultiViews
              AllowOverride All
              Order allow,deny
              allow from all
          </Directory>
      </VirtualHost>

3. Edit ``/etc/httpd/conf.d/wsgi.conf`` file::

      LoadModule wsgi_module modules/mod_wsgi.so
      <IfModule mod_wsgi.c>
          AddHandler wsgi-script .wsgi
          Include /var/www/html/mytardis/apache/apache_django_wsgi.conf
      </IfModule>
  
4. Create ``apache_django_wsgi.conf`` file::

      cd /var/www/html/mytardis/apache/
      cp apache_django_wsgi.conf_changeme apache_django_wsgi.conf

5. Edit the ``apache_django_wsgi.conf`` file as shown below::

      Alias /static/ /var/www/html/mytardis/static/
      <Directory /var/www/html/mytardis/static/>
      Order deny,allow
      Allow from all
      </Directory>
      
      WSGIScriptAlias / "/var/www/html/mytardis/apache/django.wsgi"
      
      <Directory "/var/www/html/mytardis/apache">
      Allow from all
      </Directory>
      
   Remember to delete or comment out all the original configuration in ``apache_django_wsgi.conf``::
   
      WSGIScriptAlias / "/Users/steve/django-jython-svn/myTARDIS_checkout/tardis/apache/django.wsgi"
      
      <Directory "/Users/steve/django-jython-svn/myTARDIS_checkout/tardis/apache">
      Allow from all
      </Directory>
      

6. Create ``django.wsgi`` file::
  
      cd /var/www/html/mytardis/apache/
      cp django.wsgi_changeme django.wsgi
  
7. Edit the ``django.wsgi`` file with instructions shown below followed by an example of django.wsgi.
  
   a. Please copy the value of **sys.path** variable from ``/opt/mytardis/bin/django.wsgi`` file.

   b. Remember to delete or comment out the following line in ``django.wsgi`` file::
   
        sys.path.append('/Users/steve/django-jython-svn/myTARDIS_checkout')
      
   c. Also change the value of DJANGO_SETTINGS_MODULE environment variable so that it points to your project’s settings.py file if necessary.
   
   d. Example::
   
        #!/usr/bin/python
      
        import os
        import sys
        sys.path[0:0] = [
            '/opt/mytardis',
            '/opt/mytardis/eggs/nose-1.1.2-py2.6.egg',
            '/opt/mytardis/eggs/coverage-3.4-py2.6-linux-x86_64.egg',
            '/opt/mytardis/eggs/django_nose-1.0-py2.6.egg',
            '/opt/mytardis/eggs/nosexcover-1.0.7-py2.6.egg',
            '/opt/mytardis/eggs/python_ldap-2.4.9-py2.6-linux-x86_64.egg',
            '/opt/mytardis/eggs/python_magic-0.4.0dev-py2.6.egg',
            '/opt/mytardis/eggs/python_memcached-1.48-py2.6.egg',
            '/opt/mytardis/eggs/pysolr-2.1.0_beta-py2.6.egg',
            '/opt/mytardis/eggs/docutils-0.8.1-py2.6.egg',
            '/opt/mytardis/eggs/flexmock-0.9.3-py2.6.egg',
            '/opt/mytardis/eggs/compare-0.2b-py2.6.egg',
            '/opt/mytardis/eggs/django_jasmine-0.3.2-py2.6.egg',
            '/opt/mytardis/eggs/celery-2.5.1-py2.6.egg',
            '/opt/mytardis/eggs/django_celery-2.5.1-py2.6.egg',
            '/opt/mytardis/eggs/django_kombu-0.9.4-py2.6.egg',
            '/opt/mytardis/eggs/iso8601-0.1.4-py2.6.egg',
            '/opt/mytardis/eggs/html2text-3.200.3-py2.6.egg',
            '/opt/mytardis/eggs/pyoai-2.4.4-py2.6.egg',
            '/opt/mytardis/eggs/Wand-0.1.9-py2.6.egg',
            '/opt/mytardis/eggs/djangorecipe-1.1.2-py2.6.egg',
            '/opt/mytardis/eggs/Django-1.3-py2.6.egg',
            '/opt/mytardis/eggs/zc.recipe.egg-1.3.2-py2.6.egg',
            '/opt/mytardis/eggs/zc.buildout-1.5.2-py2.6.egg',
            '/opt/mytardis/eggs/lxml-2.2.7-py2.6-linux-x86_64.egg',
            '/opt/mytardis/eggs/django_picklefield-0.2.0-py2.6.egg',
            '/opt/mytardis/eggs/ordereddict-1.1-py2.6.egg',
            '/opt/mytardis/eggs/python_dateutil-1.5-py2.6.egg',
            '/opt/mytardis/eggs/kombu-2.1.3-py2.6.egg',
            '/opt/mytardis/eggs/anyjson-0.3.1-py2.6.egg',
            '/opt/mytardis/eggs/importlib-1.0.2-py2.6.egg',
            '/opt/mytardis/eggs/setuptools-0.6c12dev_r88846-py2.6.egg',
            '/opt/mytardis/eggs/httplib2-0.7.4-py2.6.egg',
            '/opt/mytardis/eggs/pytz-2012b-py2.6.egg',
            '/opt/mytardis/eggs/South-0.7.4-py2.6.egg',
            '/opt/mytardis/eggs/BeautifulSoup-3.2.1-py2.6.egg',
            '/opt/mytardis/eggs/django_haystack-1.2.6-py2.6.egg',
            '/opt/mytardis/eggs/django_form_utils-0.2.0-py2.6.egg',
            '/opt/mytardis/eggs/django_extensions-0.8-py2.6.egg',
            '/opt/mytardis/eggs/django_registration-0.8-py2.6.egg',
            '/opt/mytardis/eggs/elementtree-1.2.7_20070827_preview-py2.6.egg',
            '/opt/mytardis/eggs/feedparser-5.1.1-py2.6.egg',
            '/opt/mytardis/eggs/amqplib-1.0.2-py2.6.egg',
            '/opt/mytardis/parts/django',
            ]
      
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tardis.settings'
        import django.core.handlers.wsgi
        application = django.core.handlers.wsgi.WSGIHandler()
      

8. As root, make all file/directories in mytardis as group apache with *rx* access permission::

      chgrp apache -R /opt/mytardis
      chmod g+w mytardis
      chmod g+rx -R /opt/mytardis
      
9. Set proper file access permission to ``/opt/mytardis/var``::

      chmod g+rwx -R /opt/mytardis/var

Step 7: SELinux
---------------
1. Disable SELinux protection in RHEL::

      setenforce 0


Step 8: Firewall Settings
-------------------------
1. Open flle ``/etc/sysconfig/iptables``::

      vi /etc/sysconfig/iptables
 
2. Append rules as follows::

      -A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
      -A INPUT -m state --state NEW -p tcp --dport 443 -j ACCEPT
 
3. Save and close the file. 
4. Restart iptables::

      /etc/init.d/iptables restart


Step 9: MicroTardis Web Portal 
------------------------------
1. Restart Apache service::

      /etc/init.d/httpd restart

2. Check if MicroTardis Web Portal is working fine via browser with URL::

      http://your.hostname.domain/
      
   For example::
   
      http://microtardis-test.eres.rmit.edu.au/
