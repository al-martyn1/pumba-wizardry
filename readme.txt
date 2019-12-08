Pumba Wizardry - The wizard engine you've ever dreamed of
(c) Alexander Martynov (amart on Mail Ru domain)


Installation:


1) Install Python (Windows installation)


   Download Python2
       x86 - https://www.python.org/ftp/python/2.7.17/python-2.7.17.msi
    or x64 - https://www.python.org/ftp/python/2.7.17/python-2.7.17.amd64.msi

   Run this setup.
      Select folder: "D:\Python27" or another as you wish.
      Select "For current user" or "For all users" as you wish.
      Select "Do not add to PATH environment variable"


   Download Python3
       x86 - https://www.python.org/ftp/python/3.8.0/python-3.8.0.exe
    or x64 - https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe

   Run this setup.
      Select "Customize Installation".
      Select folder: "D:\Python38" or another as you wish.
      Optionally check both "Debug" checkboxes for native debugging.
      Select "For all users" as you wish.
      !!! Important: Select "Py Launcher" checkbox


   Now Python3 will be used by default, but you can lauch Python2 or Python3 
   using py2 or py3 commands


2) Install required Python modules

   Open console (cmd or git bash).

   Run:

       "pip install commentjson" - for install optional module wich allows you 
                                   to use comments in wizard jaysons.

       "pip install pyqt5" - for install required GUI module PyQt5

       "pip install mako"  - for install required templating module Mako
                             https://docs.makotemplates.org/en/latest/usage.html


   If you got an errors, try next:

       Rollback PIP to 18.1:

           "pip install pip==18.1"

       Install required module, e.g:
       
           "pip install commentjson"

       Upgrade PIP back to the latest version:

           "python -m pip install –upgrade pip"


3) Install Pumba Wizardry

   Open console (cmd or git bash).

   Run:

       "git clone https://github.com/al-martyn1/pumba-wizardry.git PW-FOLDER-NAME"

       where "PW-FOLDER-NAME" is the folder where you want to install
           "Pumba Wizardry", e.g. "D:\PumbaWizardry", "D:\pumba_wizardry" or
           "D:\pumba-wizardry"

       *NOTE: Spaces are acceptable, but a name without spaces and national
              characters is considered a good form of folder name.


   Add "PW-FOLDER-NAME\super-pumba" folder to "PATH" environment variable 
       to get access to "Pumba Wizardry Super Pumba Super Wizard" from whatever.

   Also, you can run "super-pumba" wizard as well as all other wizards using fully specified path.


4) Install or create your "Pumba Wizardry"-powered wizards

   "Pumba Wizardry" wizard library organized into two level hierachy:
       wizard's family folder and separate wizard folders under wizard family folder.

   Wizard library is located under "PW-FOLDER-NAME\wizards" path.
   Your can clone your shared wizard family repos into that folder or create your 
       wizard families and wizards inplace under wizards root.

   If your want to get access to your wizards in command line from whatever,
       separate add each wizard family path to "PATH" environment variable.


5) Enjoy with "Pumba Wizardry"!

   Run "PW/super-pumba/super-pumba.bat" to list all of the wizards and select apropriate one.

   Run "PW/wizards/FAMILY/WIZARD.bat" to run the exact wizard.
