.. _installation:

************************************
Installing Your MicroTardis Instance
************************************

This document describes a step by step guide on how to install MicroTardis/MyTardis system.
The documentation includes two main parts: the first part describes the installation
of MyTardis system and MicroTardis extensions; and the second part is the instructions of  
deploying MicroTardis within RMIT ITS network.


.. _installing_microtardis:

Installing MicroTardis
======================

**Please note that these installation instructions were written based on a MyTardis 2.5 installation on RHEL 6 with a root permission.**

Step 1: Internet Proxy Settings if Within RMIT Network
------------------------------------------------------

**Please skip this step if your machine isn't hosted within RMIT network.**

If you would like to install MicroTardis in a RMIT machine, it's required to have RMIT HTTP/HTTPS proxy settings to access the Internet. 

1. Copy the following lines into ``/etc/environment`` with root permission to have system-wide proxy settings::
   
      http_proxy=http://bproxy.rmit.edu.au:8080
      https_proxy=http://bproxy.rmit.edu.au:8080   
   
2. Save the file and re-login. 
3. To make sure the setting is there by opening a terminal and issuing the command::

      export | grep -i proxy
      
   then you should see the proxy settings as what you have just configured.


Step 2: Prerequisites
---------------------
MicroTardis is currently only supported on RHEL and Ubuntu with SELinux disabled.

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
    
    
Step 3: Download MyTardis Source Code
-------------------------------------
1. Get the **MyTardis 2.5 release branch** and check out the source code into ``/opt/`` directory::

      cd /opt
      git clone git://github.com/mytardis/mytardis.git
      cd mytardis
      git tag -l
      git checkout 2.5.0-rc1

2. If you get *an error of connection timed out* as shown below::

      Initialized empty Git repository in /opt/mytardis/.git/
      github.com[0: 207.97.227.239]: errno=Connection timed out
      fatal: unable to connect a socket (Connection timed out)

   Please use the following commands instead (cloning GitHub repository over HTTP/HTTPS)::

      cd /opt
      git config --global http.proxy bproxy.rmit.edu.au:8080
      git clone https://github.com/mytardis/mytardis.git
      cd mytardis
      git tag -l
      git checkout 2.5.0-rc1

   It might be slow and recommended to be used if the git port(9418) is blocked due to a firewall constraint.


Step 4: Download MicroTardis Extensions
---------------------------------------
1. To get the current master branch of MicroTardis and install it inside MyTardis folder::

      cd /opt/mytardis/tardis
      git clone https://github.com/mytardis/microtardis.git
   
   The ``microtardis`` directory should be the same level as the ``tardis_portal`` directory.
   
Step 5: Building
---------------------------

MicroTardis/MyTardis is using the Buildout build system to handle the installation of dependencies and create the python class path.
   
1. Run the Buildout bootstrap script to initialise Buildout::

      cd /opt/mytardis
      python bootstrap.py
   
2. Download and build Django and all dependencies::

      cd /opt/mytardis
      bin/buildout
   
   *This can be run again at any time to check for and download any new dependencies.* 

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

   If you encountered an error looks like::
   
      _mysql_exceptions.OperationalError: (1170, "BLOB/TEXT column 'string_value' used in key specification without a key length")
   
   Please ignore it for the moment. It's a bug in MyTardis, and hopefuly they 
   will fix it soon in next version of MyTardis. If you would like to know what 
   the actual cause of this error is, please refer to `MERROR 1170 (42000) <http://www.mydigitallife.info/mysql-error-1170-42000-blobtext-column-used-in-key-specification-without-a-key-length/>`_ 
   for more details. 
   
   
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
In MyTardis/MicroTardis, **staging area** is an intermediate data storage area 
between the sources of raw data and the MyTardis/MicroTardis **data store**.
It is used for gathering data from different sources that will be ready to 
ingest into MyTardis/MicroTardis data store at different times. 

With respect to the solution of automatic data collection on staging area, please see an 
example of `RMIT MicroTardis Data Harvest <http://microtardis.readthedocs.org/en/latest/install_scripts.html>`_ for more details.

1. The default location of staging area or data store is in ``mytardis/var``. If you have followed the installation instructions above, you should be able to see them:: 

   /opt/mytardis/var/staging
   /opt/mytardis/var/store

2. Specify a directory path of your own staging area or data store (Optional).
 
   a. Edit your settings.py file, for example::
   
        vi /opt/mytardis/tardis/settings.py
   
   b. Find the following lines in the settings.py file::
   
        #STAGING_PATH = '/directory/path/of/your/own/staging'
        #FILE_STORE_PATH = '/directory/path/of/your/own/store'
     
   c. Uncomment the line and specify the location of your own staging area or data store.

3. Set up remote staging area and data store (Optional).

   If you need to use remote or mounted staging/store area, please create symbolic links in ``/opt/mytardis/var`` to replace default staging and store directories.
   
   a. Create a symbolic link for ``staging`` area from MicroTardis to the remote storage::

        cd /opt/mytardis/var
        rmdir staging
        ln -s /mnt/your_remote_staging staging
    
   b. Create a symbolic link for ``store`` from MicroTardis to the remote storage::

        cd /opt/mytardis/var
        rmdir store
        ln -s /mnt/your_remote_store store

4. Create **MicroTardis Staging Structure** for data ingestion from staging area into MicroTardis data store.

   In MicroTardis, it needs a certain folder structure inside staging to enable data ingestion. 
   
   a. The first thing to do is to create user folders inside your staging area::

        cd /opt/mytardis/var/staging
        mkdir your_username
      
      You can use the administrator account that you've just created.
      
   b. Then create folders for microscope instruments. So far, MicroTardis supports 3 different microscopes,
   
      * Philips XL30 SEM (1999) with Oxford Si(Li) X-ray detector and HKL EDSD system
      * FEI Nova NanoSEM (2007) with EDAX Si(Li)X-ray detector
      * FEI Quanta 200 ESEM with EDAX Si(Li) X-ray detector and Gatan Alto Cyro stage 
   
      Please name your microscope folders as,
      
      * XL30
      * NovaNanoSEM
      * Quanta200  

      For example::
      
        cd /opt/mytardis/var/staging/your_username
        mkdir NovaNanoSEM

5. Copy example files into your microscope folders.

   Here are some example files for you to download,
   
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
   
   Then you will be able to see the folders/files you've just created/downloaded on *MicroTardis Create Experiment* web interface.


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
  
   a. Please copy the value of **sys.path** variable from ``/opt/mytardis/bin/django.wsgi`` file which is a list of full directory paths of modules required by MicroTardis.

   b. Remember to delete or comment out the following line in your ``django.wsgi`` file::
   
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
      chmod g+w /opt/mytardis
      chmod g+rx -R /opt/mytardis
      
9. Set proper file access permission to ``/opt/mytardis/var`` directory::

      chmod g+rwx -R /opt/mytardis/var

Step 7: SELinux
---------------
1. Disable SELinux protection in RHEL.

   a. To turn SELinux off immediately, without rebooting use (turning off SELinux temporarily)::
   
        setenforce 0

   b. Completely turning off SELinux,

      Edit ``/etc/selinux/config`` (e.g. $sudo vi /etc/selinux/config).
      
      Find the line::
      
        SELINUX=enforcing

      If you simply want to set selinux to *permissive* mode which will still warn you when something would have been denied, change it to::

        SELINUX=permissive
        
      If you want to completely disable SELinux, change it to::

        SELINUX=disabled
      
      Save the file, then you will need to reboot your system to create the desired effect. 

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
1. Configure Apache to run every time the system starts::

      chkconfig httpd on
      
2. Test if Apache service is running::

      service httpd status
     
3. Start Apache service,

   a. Simply start Apache service if it's not running::
    
        service httpd start
                
   b. Restart Apache service if it's already running::
    
        service httpd restart

4. Check if MicroTardis Web Portal is working fine via browser with URL::

      http://your_hostname.domainname/
      
   For example::
   
      http://microtardis-test.eres.rmit.edu.au/

   If everything works fine, then you will be able to see MicroTardis's Welcome web page.