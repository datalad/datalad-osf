DataLad extension to interface with OSF
***************************************

Welcome! This extension equips DataLad with tools to interoperate with projects on the Open Science Framework (OSF). Specifically, it can create a git-annex special remote implementation to transform OSF storage into git-annex repositories. Files in OSF storage could thus be consumed or exported fast and easily via git-annex or DataLad, and published to repository-hosting services (GitHub, GitLab, Bitbucket, ...) as lightweight repositories that constitute an alternative access to the data stored on the OSF - that is: you can git clone a repository from for example GitHub and get the data from the OSF from the command line or in your scripts.

The extension was created during the OHBM Hackathon 2020.


.. toctree::

   acknowledgments

Documentation
=============

.. toctree:: 
   :maxdepth: 2

   intro
   settingup
   running
   example
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
