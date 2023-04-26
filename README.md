Make sure you have python installed in your system.

If not. To install python refer to the below link and install python according to your system config.

https://www.python.org/downloads/


Make sure you have pip installed in your system.
If not, To install pip refer to the below link and install pip according to your system config.

https://pip.pypa.io/en/stable/installation/


First, run the below command

**pip3 install -r requirements.txt**



Once requirements are installed. Run the below command to run the migrations

**python manage.py migrate**


To list the available commands, run the below command

**python manage.py show_available_commands**


You will be able to see commands like **login, signup, follow**, etc.

The commands listed can be used in the following manner.

**python manage.py {command_name} {options}**

**Ex: python manage.py signup hitesh hitesh**


To view the required parameters for the command run the below command

**python manage.py {command_name} --help**


**It will show what the command does and mention the required and optional arguments for the command and will list the mandatory required arguments under the postional arguments section.**

Enjoy!
