MicroTardis Administration Guide
================================

Create New Users
----------------
MicroTardis has two authentication methods. One is **local** user authentication 
which is the preferred solution using a local authentication database. In this 
case, site administrator is required to perform user account maintenance and 
validation tasks. For each valid user, site administrator has to manually create
a user account with a username and a password and grant this user proper 
privileges to register this user in MicroTardis.

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


Sign in MicroTardis Administration Interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#. Log in MicroTardis administration interface via MicroTardis login page with
   your administrator account. 

   .. image:: _static/createuser_admin_login.png 

#. Click on your username in the top left-hand corner of the screen to access to
   MicroTardis administration tool.

   .. image:: _static/createuser_link_to_admin_tool.png 

#. Then you will see the following page if you've signed in with your 
   administrator account successfully. 

   .. image:: _static/createuser_admin_tool.png 
   
Create Data in Three Related Tables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You will have to add objects into the following three different tables to 
complete the process of creating a user account.

   * Users
   * User profiles
   * User authentications
   
The following three subsections will show you how to do that.

Add a User 
~~~~~~~~~~
#. First of all, find **Users** in **Auth** box on your administration home page 
   and click on it.
   
   .. image:: _static/createuser_users_table.png 
   
#. Then you will see the following page showing **Users** data table. Click on 
   **Add user** in the top right-hand corner of the screen.
   
   .. image:: _static/createuser_create_user_link.png 
   
#. Input username and assign a temporary password to the user. Click on **Save**
   button in the bottom right-hand corner to create a user object.
   
   .. image:: _static/createuser_save_user.png 
   
#. Continue to edit user's personal info,
   
   .. image:: _static/createuser_user_personal_info.png 
   
#. (Optional) Tick the checkbox of **Staff status** to mark the user as a 
   *staff* member if you would like to create a MicroTardis site administrator 
   account. Once the user is marked as a *staff* member, and thus is allowed 
   access to the administration interface.
   
   .. image:: _static/createuser_staff.png 
   
#. (Optional) Tick the checkbox of **Superuser status** to mark the user as a 
   *superuser* member if you would like to create a super account with full 
   access and data management control. Once the user is marked as a *superuser* 
   member, and thus is assigned all permissions.
   
   .. image:: _static/createuser_superuser.png 
   
#. Assign basic access permissions for a regular user. Three basic user 
   permissions are recommended,

   * Can add experiment
   * Can change experiment
   * Can change experiment acl
   
   to allow users to create/edit their own experiments and manage experiment 
   access. The following three steps will show you how to do it.
   
   a. Select the three basic access permissions from **Available user 
      permissions** box,
   
      .. image:: _static/createuser_choose_basic_user_permission.png 
   
   b. Click on the *right arrow button* right next to the **Available user 
      permissions** box.
   
      .. image:: _static/createuser_assign_basic_user_permission.png 
   
   c. Then you will see the chosen permissions are on the **Chosen user 
      permissions** box.
   
      .. image:: _static/createuser_chosen_user_permissions.png 
   
#. Leave everything else as default, then click on **Save** button on the same 
   page to finish editing user's info and basic permissions.
   
   .. image:: _static/createuser_save_user_info_and_permission.png 
   
Add a User Profile
~~~~~~~~~~~~~~~~~~
   
#. Go back to MicroTardis administration interface home page. Find 
   **User profiles** in **Tardis_Portal** box and click on it.
   
   .. image:: _static/createuser_user_profiles_table.png  
   
#. Then you will see the following page showing **User profiles** data table. 
   Click on **Add user profile** in the top right-hand corner of the screen.
   
   .. image:: _static/createuser_create_user_profile_link.png      
   
#. Choose the user object that you just created, then click on **Save** button 
   in the bottom right-hand corner to create a user profile object.

   .. image:: _static/createuser_save_user_profile.png 
   
Add a User Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~
#. Go back to MicroTardis administration interface home page. Find **User 
   authentications** in **Tardis_Portal** box and click on it.
   
   .. image:: _static/createuser_user_authentications_table.png    
   
#. Then you will see the following page showing **User authentications** data 
   table. Click on **Add user authentication** in the top right-hand corner of 
   the screen.
   
   .. image:: _static/createuser_create_user_authentication_link.png    
   
#. Choose the UserProfile object that you just created, give a Username, and 
   specify AuthenticationMethod as **localdb**. Then click on **Save** 
   button in the bottom right-hand corner to create a user authentication 
   object.

   .. image:: _static/createuser_save_user_authentication.png    
   

Create New Groups
----------------------
Group is a mechanism to allow user to share experiences and associated 
datasets/datafiles with other ones in the same group. Regular users don't have 
permission to create groups. Only site administrators and superusers can do it.

#. Go back to MicroTardis administration interface home page. Find **Groups** in
   **Auth** box and click on it.
   
   .. image:: _static/createuser_user_authentications_table.png   


Assign Group Owners
-------------------
You have two ways to assign an administrator/owner to a group

1. via MicroTardis web portal

2. via MicroTardis administration interface

Manage Group Members
--------------------

Experiment Access Controls
--------------------------

Publish Experiment
------------------