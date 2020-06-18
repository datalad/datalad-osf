DataLad extension to interface with OSF
***************************************

This extension aims to allow DataLad to work with the Open Science Framework (OSF). This is done by transforming storage on the Open Science Framework (OSF) into a `git-annex <https://git-annex.branchable.com/>`_  repository. You can use this extension to use the OSF as a special remote to store data in the annex  of a dataset. With this, you can `datalad publish` a dataset to GitHub or similar services and the data to the OSF (via a publication dependency).

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
   exportgitannexdata
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

   osf_cmd


Command line reference
----------------------

.. toctree::
   :maxdepth: 1

   generated/man/datalad-osf-cmd



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
