MicroTardis Administration Guide
================================

Create New Users
----------------
MicroTardis has authentication integrated with 
`RMMF Booking System (EMBS) <http://embs.set.rmit.edu.au/mebookings.php>`_. It
automatically create new user account when RMMF user first login to MicroTardis 
using the same username and password in EMBS.

However, MicroTardis allows site administrator to manually create user account
as well via MicroTardis admin tool. The following steps will show you how to
create user account via its admin interface.

Login to MicroTardis Admin Interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#. Login to MicroTardis admin interface via MicroTardis login page with your administrator account. 

   .. image:: _static/createuser_admin_login.png 

#. Click on your username in the top left-hand corner of the screen to access to MicroTardis admin tool.

   .. image:: _static/createuser_link_to_admin_tool.png 

#. Then you will see the following page if you've signed in to your administrator account successfully. 

   .. image:: _static/createuser_admin_tool.png 
   
Three Related Tables for Users
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You will have to add objects into the following three different tables to complete the process of creating a user account.

   * Users
   * User profiles
   * User authentications
   
The following subsections will provide more details.

Add a User 
^^^^^^^^^^
#. First of all, find **Users** in **Auth** table and click on it.
   
   .. image:: _static/createuser_users_table.png 
   
#. Then you will see the following page showing **Users** table. Click on **Add user** in the top right-hand corner of the screen.
   
   .. image:: _static/createuser_create_user_link.png 
   
#. Input username and assign a temporary password to the user. Click on **Save** button in the bottom right-hand corner to create a user object.
   
   .. image:: _static/createuser_save_user.png 
   
#. Continue to edit user's personal info,
   
   .. image:: _static/createuser_user_personal_info.png 
   
#. Tick the checkbox of **Staff status** to mark the user as a *staff* member if need be. Once the user is marked as a *staff* member, and thus is allowed access to the admin interface.
   
   .. image:: _static/createuser_staff.png 
   
#. Tick the checkbox of **Superuser status** to mark the user as a *superuser* member if need be. Once the user is marked as a *superuser* member, and thus is assigned all permissions.
   
   .. image:: _static/createuser_superuser.png 
   
#. Assign basic access permissions to the user. Three basic user permissions are recommended,

   * Can add experiment
   * Can change experiment
   * Can change experiment acl
   
   to allow users to create/edit their own experiments and manage experiment access. 
   
#. Select the three basic access permissions from **Available user permissions** box,
   
   .. image:: _static/createuser_choose_basic_user_permission.png 
   
#. Click on the *right arrow button* right next to the **Available user permissions** box.
   
   .. image:: _static/createuser_assign_basic_user_permission.png 
   
#. Then you will see the chosen permissions are on the **Chosen user permissions** box.
   
   .. image:: _static/createuser_chosen_user_permissions.png 
   
#. Leave everything else as default, then click on **Save** button on the same page to finish editing user's info and basic permissions.
   
   .. image:: _static/createuser_save_user_info_and_permission.png 
   
Add a User Profile
^^^^^^^^^^^^^^^^^^
   
#. Go back to MicroTardis admin interface home page. Find **User profiles** in **Tardis_Portal** table and click on it.
   
   .. image:: _static/createuser_user_profiles_table.png  
   
#. Then you will see the following page showing **User profiles** table. Click on **Add user profile** in the top right-hand corner of the screen.
   
   .. image:: _static/createuser_create_user_profile_link.png      
   
#. Choose the user that you just created, then click on **Save** button in the bottom right-hand corner to create a user profile object.

   .. image:: _static/createuser_save_user_profile.png 
   
Add a User Authentication
^^^^^^^^^^^^^^^^^^^^^^^^^
#. Go back to MicroTardis admin interface home page. Find **User authentications** in **Tardis_Portal** table and click on it.
   
   .. image:: _static/createuser_user_authentications_table.png    
   
#. Then you will see the following page showing **User authentications** table. Click on **Add user authentication** in the top right-hand corner of the screen.
   
   .. image:: _static/createuser_create_user_authentication_link.png    
   
#. Choose the **UserProfile** that you just created, give a **Username**, and specify **AuthenticationMethod** with **localdb**. Then click on **Save** button in the bottom right-hand corner to create a user authentication object.

   .. image:: _static/createuser_save_user_authentication.png    
   

Create New Groups
----------------------
Group is a mechanism to allow user to share experiences and associated 
datasets/datafiles with other ones in the same group. Regular users don't have 
permission to create groups. Only site administrators and superusers can do it.

#. Go back to MicroTardis admin interface home page. Find **Groups** in **Auth** table and click on it.
   
   .. image:: _static/createuser_user_authentications_table.png   


Assign Group Owners
-------------------
You have two ways to assign an administrator/owner to a group

1. via MicroTardis web portal

2. via MicroTardis admin tool

Manage Group Members
--------------------

Experiment Access Controls
--------------------------