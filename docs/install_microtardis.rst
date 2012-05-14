.. _installation:

************************************
Installing Your MicroTardis Instance
************************************

This document describes a step by step guide on how to install 
MicroTardis/MyTardis system. The documentation includes two main parts: the 
first part describes the installation of MyTardis system and MicroTardis 
extensions; and the second part is the instructions of deploying MicroTardis 
within RMIT ITS network.


.. _installing_microtardis:

Installing MicroTardis
======================

**Please note that these installation instructions were written based on a 
MyTardis 2.5 installation on RHEL 6 with a root permission.**

Step 1: Internet Proxy Settings if Within RMIT Network
------------------------------------------------------

**Please skip this step if your machine isn't hosted within RMIT network.**

If you would like to install MicroTardis in a RMIT machine, it's required to 
have RMIT HTTP/HTTPS proxy settings to access the Internet. 

#. Copy the following lines into ``/etc/environment`` with root permission to 
   have system-wide proxy settings::
   
      http_proxy=http://bproxy.rmit.edu.au:8080
      https_proxy=http://bproxy.rmit.edu.au:8080   
   
#. Save the file and re-login. 
#. To make sure the setting is there by opening a terminal and issuing the 
   command::

      export | grep -i proxy
      
   then you should see the proxy settings as what you have just configured.


Step 2: Prerequisites
---------------------
MicroTardis is currently only supported on RHEL and Ubuntu with SELinux 
disabled. The following packages are essential to be system-wide installed. 

#. Redhat::

      yum install git gcc gcc-c++ httpd mod_wsgi mysql mysql-server MySQL-python 
      yum install python python-devel python-setuptools libjpeg-devel numpy python-matplotlib
      yum install cyrus-sasl-ldap cyrus-sasl-devel openldap-devel libxslt libxslt-devel libxslt-python
      easy_install PIL

#. Ubuntu::

      apt-get install git gcc libapache2-mod-wsgi mysql mysql-server python-mysqldb 
      apt-get instlal python python-dev python-setuptools python-numpy python-matplotlib
      apt-get install libpq-dev libssl-dev libsasl2-dev libldap2-dev libxslt1.1 libxslt1-dev python-libxslt1 libexiv2-dev
      easy_install PIL
    
    
Step 3: Download MyTardis Source Code
-------------------------------------
#. Check out MyTardis source code into ``/opt/`` directory::

      cd /opt
      git clone git://github.com/mytardis/mytardis.git

   If you get an error of **Connection timed out** as shown below::

      Initialized empty Git repository in /opt/mytardis/.git/
      github.com[0: 207.97.227.239]: errno=Connection timed out
      fatal: unable to connect a socket (Connection timed out)

   It means that the git port (9418) might be blocked due to a firewall 
   constraint. Please try the following commands to clone GitHub repository over 
   HTTP/HTTPS instead::

      cd /opt
      git config --global http.proxy bproxy.rmit.edu.au:8080
      git clone https://github.com/mytardis/mytardis.git


   It might be slow and recommended to be used if the git port(9418) is blocked.

#. Get the **MyTardis 2.5 release branch**::

      cd mytardis
      git tag -l
      git checkout 2.5.0-rc1

   then you will see messages similar to the one below::
   
      Note: checking out '2.5.0-rc1'.

      You are in 'detached HEAD' state. You can look around, make experimental
      changes and commit them, and you can discard any commits you make in this
      state without impacting any branches by performing another checkout.

      If you want to create a new branch to retain commits you create, you may
      do so (now or later) by using -b with the checkout command again. Example:

        git checkout -b new_branch_name

      HEAD is now at 9615e03... Merge pull request #64 from shaunokeefe/sync-rebased
      
   it means that you have checked out '2.5.0-rc1' branch successfully.
    

Step 4: Download MicroTardis Extensions
---------------------------------------
#. To get the current master branch of MicroTardis and install it inside 
   MyTardis folder::

      cd /opt/mytardis/tardis
      git clone https://github.com/mytardis/microtardis.git
   
   Please note that it is essential to check out ``microtardis`` source codes 
   into ``/opt/mytardis/tardis`` directory where the ``tardis_portal`` directory 
   is. The tardis_portal directory contains main functions of MyTardis. It is
   necessary for MicroTardis to live in the same location of it to reuse or 
   override its features.
   
   
Step 5: Building
---------------------------

MicroTardis/MyTardis uses the Buildout Python-based build system to 
automatically create, assemble and deploy applications or modules required 
by MicroTardis/MyTardis project. It would automatically download and install the 
modules and their dependencies inside ``/opt/mytardis`` directory. Please note 
that this is not a system-wide installation. Buildout uses a Python tool called 
setuptools internally to install the packages. 
   
#. Run the **bootstrap** script to bootstrap a buildout-based project::

      cd /opt/mytardis
      python bootstrap.py
   
#. Run the **buildout** script to download and install Python eggs and all 
   dependencies::

      cd /opt/mytardis
      bin/buildout
   
   *This can be run again at any time to check for and download any new 
   dependencies.* 
   
Deploying MicroTardis
=====================

Step 6: MicroTardis settings.py File
------------------------------------

Configuring MicroTardis/MyTardis is done through a standard Django *settings.py* 
file. MyTardis comes with a sample configuration file at 
``/opt/mytardis/tardis/settings_changeme.py``. In MicroTardis, there is also a
settings file called ``/opt/mytardis/tardis/microtardis/settings_microtardis.py``  
which is an extension of ``/opt/mytardis/tardis/settings_changeme.py`` that 
includes support to MicroTardis application. 
   
#. To create a settings.py file for your deployment, just copy the file 
   ``/opt/mytardis/tardis/microtardis/settings_microtardis.py`` into the 
   directory where ``settings_changeme.py`` is in::

      cp /opt/mytardis/tardis/microtardis/settings_microtardis.py /opt/mytardis/tardis/settings.py

#. To configure MicroTardis for interactive use to proceed following parts of 
   configuration, please edit the file ``/opt/mytardis/bin/django`` and replace 
   the following line::

       djangorecipe.manage.main('tardis.test_settings')

   with::
    
       djangorecipe.manage.main('tardis.settings')
    
   This means that the ``/opt/mytardis/bin/django`` command will run the 
   interactive configuration rather than the test configuration. And we will use
   this command later on to manually create database tables or superuser, and so 
   on.

Step 7: MicroTardis Database
----------------------------
#. Ensure that the MySQL database has been started::
   
      /etc/init.d/mysqld start
   
#. Configure MySQL to run every time the system starts::

      chkconfig mysqld on

#. Create a database named **microtardis**::

      mysql -e "CREATE DATABASE microtardis"
      
#. Run the following command to configure the database, and create user account
   and password; don't forget to replace **'microtardisuser'** and **'secret'** 
   with a user name and a password of your choices::

      mysql -e "GRANT ALL PRIVILEGES ON microtardis.* TO 'microtardisuser'@'localhost' IDENTIFIED BY 'secret';"
   
#. Edit the ``/opt/mytardis/tardis/settings.py`` file which you have just 
   created in former step. Please ensure that the values of database parameters 
   in settings.py match the values used to create your MicroTardis database::

      DATABASES = {}
      DATABASES['default'] = {}
      DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
      DATABASES['default']['HOST'] = 'localhost'
      DATABASES['default']['PORT'] = '3306'
      DATABASES['default']['NAME'] = 'microtardis'
      DATABASES['default']['USER'] = 'microtardisuser'
      DATABASES['default']['PASSWORD'] = 'secret'
      
   This is the minimum set of changes required to successfully run the server. 
   You can make any other site-specific changes in 
   ``/opt/mytardis/tardis/settings.py`` as necessary.

#. (OPTIONAL) For the purpose of database maintenance, you might need to have 
   root access to MySQL database. If you have root access, run the following 
   command to ensure that the MySQL instance has a root password; don't forget 
   to replace the word *'rootsecret'* with a password of yours::

      mysqladmin password rootsecret

   If you need to reset MySQL root password, then run the following command to 
   reset the password of your choice::

      mysqladmin -u root -pcurrentpassword password 'newpassword'

   Please note that there is no space between **-p** and **currentpassword**. Or
   you can also change MySQL root password from MySQL prompt using UPDATE SQL 
   command::

      mysql> UPDATE user SET password=PASSWORD('newpassword') WHERE user='root';
      mysql> FLUSH PRIVILEGES;
      mysql> EXIT;

   Once you've changed it, make sure you can login with your new password 
   successfully. And now kill your running MySQL deamon, then restart it normally.

#. Rename ``/opt/mytardis/tardis/tardis_portal/fixtures/initial_data.json`` to 
   ignore importing synchrotron-specific metadata schema::

      cd /opt/mytardis/tardis/tardis_portal/fixtures/
      mv initial_data.json initial_data.json.ignored
      
   The synchrotron-specific metadata schema is part of default schema in 
   MyTardis 2.5 release branch. However MicroTardis doesn't use it for 
   microscopy metadata data. 

#. Run the following command to setup the database tables in the MySQL database::

      cd /opt/mytardis
      bin/django syncdb --noinput --migrate 

   If you encountered an error looks like::
   
      _mysql_exceptions.OperationalError: (1170, "BLOB/TEXT column 'string_value' used in key specification without a key length")
   
   Please ignore it for the moment. It's a bug in MyTardis, and hopefuly they 
   will fix it soon in next version of MyTardis. If you would like to know what 
   the actual cause of this error is, please refer to 
   `MERROR 1170 (42000) <http://www.mydigitallife.info/mysql-error-1170-42000-blobtext-column-used-in-key-specification-without-a-key-length/>`_ 
   for more details. 
   
   
Step 8: MicroTardis Administrator
---------------------------------
1. Create an administrator account::

      cd /opt/mytardis
      bin/django createsuperuser

   Please keep your user name and password. You will need them to sign in 
   MicroTardis administrator web interface.

Step 9: Static Files
--------------------
For performance reasons you should avoid static files being served via the 
application, and instead serve them directly through the webserver.

#. To collect all the static files to a single directory::

      cd /opt/mytardis
      bin/django collectstatic


Step 10: MicroTardis Staging Area and Store
-------------------------------------------
In MyTardis/MicroTardis, **staging area** is an intermediate data storage area 
between the sources of raw data and the MyTardis/MicroTardis **data store**.
It is used for gathering data from different sources that will be ready to 
ingest into MyTardis/MicroTardis data store at different times. 

#. Setup MicroTardis staging area and data store   

   The default location of staging area or data store is in ``mytardis/var``. If 
   you have followed the installation instructions above, you should be able to 
   see them:: 

     ls -dl /opt/mytardis/var/staging
     ls -dl /opt/mytardis/var/store

   You might have noticed that both of them are empty directories. In 
   MicroTardis, data store is a file storage to keep ingested files with its 
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

        cd /opt/mytardis/var/staging
        mkdir your_username
      
      You can use the administrator account that you've just created.
      
   b. Then create **microscope folders** inside user folders with any name of 
      microscope which is currently supported in MicroTardis: XL30, NovaNanoSEM,
      and Quanta200. For example::
      
        cd /opt/mytardis/var/staging/your_username
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
   on *MicroTardis Create Experiment* web interface later after you successfully 
   start your deployment server.
   
#. (OPTIONAL) Specify directory paths of your own staging area and data store if 
   you would clike to change the locations of them instead of using the default 
   ones.
 
   a. Edit your settings.py file, for example::
   
        vi /opt/mytardis/tardis/settings.py
   
   b. Find the following lines in the settings.py file::
   
        #STAGING_PATH = '/directory/path/of/your/own/staging'
        #FILE_STORE_PATH = '/directory/path/of/your/own/store'
     
   c. Uncomment the line and specify the real location of your own staging area 
      or data store.

#. (OPTIONAL) Set up remote staging area and data store.

   If you need to use remote or mounted staging/store area, please create 
   symbolic links in ``/opt/mytardis/var`` to replace default staging and store
   directories.
   
   a. Create a symbolic link for ``staging`` area from MicroTardis to the remote 
      storage::

        cd /opt/mytardis/var
        rmdir staging
        ln -s /mnt/your_remote_staging staging
    
   b. Create a symbolic link for data ``store`` from MicroTardis to the remote 
      storage::

        cd /opt/mytardis/var
        rmdir store
        ln -s /mnt/your_remote_store store

#. (OPTIONAL) With respect to automatic data collection on staging area which 
   automatically harvests data from data sources into staging area, please see 
   an example of `RMIT MicroTardis Data Harvest <http://microtardis.readthedocs.org/en/latest/install_autoingest_at_rmmf.html>`_ 
   for more details.

Step 11: Apache and mod_wsgi
----------------------------
#. Create a symbolic link from MyTardis to standard ``/var/www/html`` structure 
   (makes a fixed path for later changes)::

      cd /var/www/html
      chmod o+w /var/www/html
      sudo -u apache ln -s /opt/mytardis mytardis
      chmod o-w /var/www/html
      
#. Set up a virtual host for MicroTardis web portal by editing 
   ``/etc/httpd/conf/httpd.conf`` file::

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

#. Edit ``/etc/httpd/conf.d/wsgi.conf`` file::

      LoadModule wsgi_module modules/mod_wsgi.so
      <IfModule mod_wsgi.c>
          AddHandler wsgi-script .wsgi
          Include /var/www/html/mytardis/apache/apache_django_wsgi.conf
      </IfModule>
  
#. Create ``apache_django_wsgi.conf`` file::

      cd /var/www/html/mytardis/apache/
      cp apache_django_wsgi.conf_changeme apache_django_wsgi.conf

#. Edit the ``apache_django_wsgi.conf`` file as shown below::

      Alias /static/ /var/www/html/mytardis/static/
      <Directory /var/www/html/mytardis/static/>
      Order deny,allow
      Allow from all
      </Directory>
      
      WSGIScriptAlias / "/var/www/html/mytardis/apache/django.wsgi"
      
      <Directory "/var/www/html/mytardis/apache">
      Allow from all
      </Directory>
      
   Remember to delete or comment out all the original configuration in 
   ``apache_django_wsgi.conf``::
   
      WSGIScriptAlias / "/Users/steve/django-jython-svn/myTARDIS_checkout/tardis/apache/django.wsgi"
      
      <Directory "/Users/steve/django-jython-svn/myTARDIS_checkout/tardis/apache">
      Allow from all
      </Directory>
      

#. Create ``django.wsgi`` file::
  
      cd /var/www/html/mytardis/apache/
      cp django.wsgi_changeme django.wsgi
  
#. Edit the ``django.wsgi`` file with instructions shown below followed by an 
   example of django.wsgi.
  
   a. Please copy the value of **sys.path** variable from 
      ``/opt/mytardis/bin/django.wsgi`` file which is a list of full directory 
      paths of modules required by MicroTardis.

   b. Remember to delete or comment out the following line in your 
      ``django.wsgi`` file::
   
        sys.path.append('/Users/steve/django-jython-svn/myTARDIS_checkout')
   
   c. Example::
   
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
      
Step 12: Permission Settings
----------------------------
MicroTardis is a Python web application. The web server (i.e. Apache) needs to 
have permissions to access the WSGI script in the directory of MicroTardis, or 
write log files or data into it. The following commands will give apache user to
do this.

#. As root, make all file/directories in mytardis as group *apache* with *rx* 
   access permission::

      chgrp apache -R /opt/mytardis
      chmod g+rx -R /opt/mytardis
     
#. Enable apache to write log files into the default directory::

      chmod g+w /opt/mytardis     
      
#. Set proper file access permission to ``/opt/mytardis/var`` directory to make
   Apache able to write data in data store::

      chmod g+rwx -R /opt/mytardis/var


Step 13: SELinux
----------------
#. Disable SELinux protection in RHEL.

   a. To turn SELinux off immediately, without rebooting use (turning off 
      SELinux temporarily)::
   
        setenforce 0

   b. Completely turning off SELinux,

      Edit ``/etc/selinux/config`` (e.g. $sudo vi /etc/selinux/config).
      
      Find the line::
      
        SELINUX=enforcing

      If you simply want to set selinux to *permissive* mode which will still 
      warn you when something would have been denied, change it to::

        SELINUX=permissive
        
      If you want to completely disable SELinux, change it to::

        SELINUX=disabled
      
      Save the file, then you will need to reboot your system to create the 
      desired effect. 

Step 14: Firewall Settings
--------------------------
#. Open flle ``/etc/sysconfig/iptables``::

      vi /etc/sysconfig/iptables
 
#. Append rules as follows::

      -A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
      -A INPUT -m state --state NEW -p tcp --dport 443 -j ACCEPT
 
#. Save and close the file. 
#. Restart iptables::

      /etc/init.d/iptables restart


Step 15: MicroTardis Web Portal 
-------------------------------
#. Configure Apache to run every time the system starts::

      chkconfig httpd on
      
#. Test if Apache service is running::

      service httpd status
     
#. Start Apache service,

   a. Simply start Apache service if it's not running::
    
        service httpd start
                
   b. Restart Apache service if it's already running::
    
        service httpd restart

#. Check if MicroTardis Web Portal is working fine via browser with URL::

      http://your_hostname.domain_name/
      
   For example::
   
      http://microtardis-test.eres.rmit.edu.au/

   If everything works fine, then you will be able to see MicroTardis's Welcome 
   web page.