DataLad extension to interface with OSF
***************************************

This extension enables DataLad to work with the Open Science Framework (OSF). Use it to publish your dataset's data to an OSF project to utilize the OSF for dataset data storage and easy dataset sharing.

The extension was created during the OHBM Hackathon 2020.


.. toctree::

   acknowledgments

Documentation
=============

.. toctree:: 
   :maxdepth: 2

   intro
   settingup
   exporthumandata
   exportdatacode
   cloneosfdata
   contact


API
===

High-level API commands
-----------------------

.. currentmodule:: datalad.api
.. autosummary::
   :toctree: generated

   create_sibling_osf


Command line reference
----------------------

.. toctree::
   :maxdepth: 1

   generated/man/datalad-create-sibling-osf



Git-annex utilities
-------------------

.. currentmodule:: datalad_osf
.. autosummary::
   :toctree: generated

   remote.OSFRemote


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |---| unicode:: U+02014 .. em dash

.. _OSF: http://www.osf.io/
