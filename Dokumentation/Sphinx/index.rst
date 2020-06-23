.. ermtk_doc documentation master file, created by
   sphinx-quickstart on Thu Oct 18 17:40:13 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. figure:: images/p185b01.png
   :align:  left

ERMTK
=====

Structure
---------
1. Help
+++++++
You can also display the whole command if you want to know which commands and parameters are available::

    ermtk --help

or::

    ermtk -h

2. Command
++++++++++
To execute the CLI use the command::

   ermtk

This command activates the ERMTK-Repl Shell.

3. Inputfile/Basic Execution
+++++++++++++++++++++++++++++++
After you have executed the command "ermtk" you have to type in the name of the input-file so the system knows from where
it should take the data. ::

   <open> "inputfile"

4. Command "list"
+++++++++++++++++

If you have used the command "open", then you are able to write following commands to list 
the data of the file: ::

Get an overview of all parameters and parameters combinations that you can use::

   list 

Get all entity-types and relationship-types with all attributes::

   list -all

or::

   list -ent -rel -attr

Get all entity-types and relationship-types::

   list -ent -rel

Get all entity-types of the file::

   list -ent

Get all entity-types with all their attributes::

   list -ent -attr

Get all relationship-types of the file::

   list -rel

Get all relationship-types with their attributes::

   list -rel -attr

Get a little information about the file::

   list -inf

.. Parameters
.. ----------
.. +------------------------+--------------------------------------------------------------------------------------------+
.. | Parameter              | Description                                                                                |
.. +========================+============================================================================================+
.. | ``--allrel``           | Generate all relationship tables                                                           |
.. +------------------------+--------------------------------------------------------------------------------------------+
.. |``--auto``              | Automatically run against database                                                         |
.. +------------------------+--------------------------------------------------------------------------------------------+
.. |``--constaft``          | Constraints inserted after create Tables                                                   |
.. +------------------------+--------------------------------------------------------------------------------------------+
.. |``--consttabl``         | Constraints inserted as table-constraints                                                  |
.. +------------------------+--------------------------------------------------------------------------------------------+
.. |``--shell``             | run a navigating shell                                                                     |
.. +------------------------+--------------------------------------------------------------------------------------------+

Example calls
-------------

Get help::

   ermtk -h

Navigate into the file fussball.prinz.xerml.xml::

   open fussball.prinz.xerml.xml

Get all entity-types of the file::

   list --ent

Get all relationship-types of the file::

   list --rel

Close the CLI::

   quit

or::

   exit